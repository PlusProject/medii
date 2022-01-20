from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import ClinicalTrials, Disease, Person, Participate, Writes, Thesis, DoctorTotalDisease, Totaldisease, DoctorAllscore
from .serializers import (ClinicalTrialsSerializer, HospitalSerializer, ThesisSerializer, NameSerializer,
                          PersonSerializer, ParticipateSerializer, WritesSerializer,
                          CrisCoworkerSerializer, ThesisCoworkerSerializer, DiseaseSerializer, DiseaseSerializer, DoctorTotalDiseaseSerializer, Totaldisease, DoctorAllscoreSerializer)
from django.db.models import Q
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
import boto3

BASE_DIR = Path(__file__).resolve().parent.parent
with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)


def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


class SearchAPI(APIView):
    def get(self, request):
        name = request.GET.get('doctor_name')
        hospital = request.GET.get('hospital')
        major = request.GET.get('major')
        disease = request.GET.get('disease')
        rare = request.GET.get('rare')

        personQuery = Person.objects.all()

        if name:
            personQuery = personQuery.filter(name_kor__icontains=name)

        if hospital:
            personQuery = personQuery.filter(belong__contains=hospital)

        if major:
            personQuery = personQuery.filter(major__contains=major)

        pid_list = [person.pid for person in personQuery]

        if disease:
            if re.compile('[a-zA-Z]\d{2}').search(disease):
                clinicalTrialsQuery = ClinicalTrials.objects.filter(
                    disease_code__icontains=disease)
            else:
                clinicalTrialsQuery = ClinicalTrials.objects.filter(
                    disease_detail__contains=disease)

            if rare == 'true':
                clinicalTrialsQuery = clinicalTrialsQuery.filter(
                    rare_disease=True)
            cid_list = [trial.cid for trial in clinicalTrialsQuery]
            pid_in_participate = []

            for cid in cid_list:
                tempQuery = Participate.objects.filter(cid=cid)
                participate_list = [p.pid.pid for p in tempQuery]
                pid_in_participate += participate_list

            pid_list = sorted((set(pid_list).intersection(pid_in_participate)))

        if re.compile('[a-zA-Z]\d{2}').search(disease):
            rare_disease = Disease.objects.filter(code=disease).values('rare')
        elif re.compile('[가-힣]+').search(disease):
            rare_disease = Disease.objects.filter(
                name_kor=disease).values('rare')
        else:
            rare_disease = Disease.objects.filter(
                name_eng=disease).values('rare')

        person = PersonSerializer(
            Person.objects.filter(pid__in=pid_list), many=True)
        return Response({
            'person': person.data,
            'rare': True if rare_disease else False
        })


class SearchClinicalTrialsAPI(APIView):
    def get(self, request):
        disease = request.GET.get('disease')
        rare = request.GET.get('rare')

        if re.compile('[a-zA-Z]\d{2}').search(disease):
            clinicalTrialsQuery = ClinicalTrials.objects.filter(
                disease_code__icontains=disease)
        else:
            clinicalTrialsQuery = ClinicalTrials.objects.filter(
                disease_detail__contains=disease)

        if rare == 'true':
            clinicalTrialsQuery = clinicalTrialsQuery.filter(rare_disease=True)
        return Response(ClinicalTrialsSerializer(clinicalTrialsQuery, many=True).data)


class ClinicalTrialsAPI(APIView):
    def get(self, request):
        pid = request.GET.get('pid')
        keyword = request.GET.get('keyword')
        participateQuery = Participate.objects.filter(pid=pid)
        participate = ParticipateSerializer(participateQuery, context={
                                            "keyword": keyword}, many=True)

        return Response(participate.data)
        # return Response({
        #     'participate': participate.data,
        #     # 'filtered_cid':
        # })


class ThesisAPI(APIView):
    def get(self, request):
        pid = request.GET.get('pid')
        writesQuery = Writes.objects.filter(pid=pid)
        writes = WritesSerializer(writesQuery, many=True)
        return Response(writes.data)


@api_view(['GET'])
def name_list(request):
    nameQuery = Person.objects.filter(job='의사').values('name_kor')
    name = NameSerializer(nameQuery, many=True)
    return Response(name.data)


@api_view(['GET'])
def hospital_list(request):
    hospitalQuery = Person.objects.filter(job='의사').values('belong').distinct()
    hospital = HospitalSerializer(hospitalQuery, many=True)
    return Response(hospital.data)


@api_view(['GET'])
def disease_list(request):
    diseases = Disease.objects.all()
    return Response(DiseaseSerializer(diseases, many=True).data)


@api_view(['GET'])
def rare_disease_list(request):
    diseases = Disease.objects.filter(rare=True)
    return Response(DiseaseSerializer(diseases, many=True).data)


@api_view(['GET'])
def get_coworker(request):
    pid = request.GET.get('pid')
    writes = Writes.objects.filter(pid=pid)
    tid_list = [thesis.tid.tid for thesis in writes]

    # coworker_list = []
    # for tid in tid_list:
    #     thesis_title = Thesis.objects.get(tid=tid).title
    #     coworker = Thesis.objects.filter(title=thesis_title)
    #     if len(coworker) > 1:
    #         coworker_list += coworker[1:]
    # print(coworker_list)
    # return Response(ThesisSerializer(coworker_list, many=True).data)
    coworker_list = []
    for tid in tid_list:
        thesis = Thesis.objects.get(tid=tid)
        thesis_title = thesis.title
        thesis_tid = thesis.tid
        coworker = Thesis.objects.filter(
            title=thesis_title).exclude(tid=thesis_tid)
        if len(coworker) > 0:
            coworker_list += coworker
    return Response(ThesisCoworkerSerializer(coworker_list, many=True).data)

# @api_view(['GET'])


class CrisCoworkerAPI(APIView):
    def get(self, request):
        pid = request.GET.get('pid')
        participate = Participate.objects.filter(pid=pid, source_name="CRIS")
        cid_list = [[cris.cid.cid, cris.position] for cris in participate]

        coworker_list = []
        for cid, position in cid_list:
            participate_list = Participate.objects.filter(
                cid=cid).exclude(position=position)
            if len(participate_list) >= 1:
                coworker_list += participate_list
        return Response(CrisCoworkerSerializer(coworker_list, many=True).data)


class RecommendAPI(APIView):

    def get(self, request):
        input = request.GET.get('input', 'I20.9')
        weight_paper = request.GET.get('weight_paper', 7)
        weight_trial = request.GET.get('weight_trial', 3)

        weight_paper = int(weight_paper)
        weight_trial = int(weight_trial)

        doctor_totaldisease = pd.DataFrame(
            list(DoctorTotalDisease.objects.all().values()))
        diseasecode_disease = pd.DataFrame(
            list(Totaldisease.objects.all().values()))
        doctor_totaldisease = doctor_totaldisease.fillna("")

        def disease_match(text):
            text = text.split(', ')
            result = dict()

            for word in text:
                disease_indexs = diseasecode_disease[diseasecode_disease['disease_code'] == word].index
                if(len(disease_indexs)):
                    result[word] = diseasecode_disease['disease_kor'][disease_indexs[0]]

            return result

        def paper_score(input, w1, w2):

            doctor_paper_data = doctor_totaldisease.copy()
            std = input.split(', ')

            def preprocess(text):
                text = text.replace('.', "dot")

                return text

            def overlap_paper(text):
                paper_overlap = 0
                papers = text.split('/ ')

                for paper in papers:
                    paper = paper.split(', ')
                    if all(temp in paper for temp in std):
                        paper_overlap += 1

                return paper_overlap

            def overlap_keyword(text):
                words_count = {}

                text = text.replace('/ ', ', ')
                words = text.split(', ')
                word_target = set(words)
                add_keyword = set(std) & word_target

                for word in words:
                    if word in words_count:
                        words_count[word] += 1
                    else:
                        words_count[word] = 1

                sorted_words = sorted(
                    [(k, v) for k, v in words_count.items()], key=lambda word_count: -word_count[1])
                keyword = [w for w in sorted_words if w[0] in add_keyword]
                if(len(keyword) >= 5):
                    keyword = keyword[0:5]

                return keyword

            def disease_kor_match(text):

                for idx in range(0, len(text)):
                    name_kor = disease_match(text[idx][0])
                    if(len(name_kor) != 0):
                        name_kor = name_kor[text[idx][0]]
                    else:
                        name_kor = 'x'
                    text[idx] = [text[idx][0], name_kor, text[idx][1]]

                return text

            target_input = preprocess(input)
            target_name = list(doctor_paper_data['name_kor'])
            target_index = len(target_name)
            target_name.append('target')

            text = list(doctor_paper_data['paper_disease_all'])
            target_text = [preprocess(t) for t in text]
            target_text.append(target_input)

            doctors = pd.DataFrame({'name': target_name,
                                    'text': target_text})

            tfidf_vector = TfidfVectorizer(min_df=3, max_features=6000)
            tfidf_matrix = tfidf_vector.fit_transform(
                doctors['text']).toarray()

            cosine_sim = cosine_similarity(tfidf_matrix)
            cosine_sim_df = pd.DataFrame(cosine_sim, columns=doctors.name)
            cosine_sim_df.head()

            temp = cosine_sim_df['target'][0:target_index]
            doctor_paper_data['cosine_simil_paper'] = temp

            doctor_paper_data['keyword_paper'] = doctor_paper_data.apply(
                lambda x: overlap_keyword(x['paper_disease_all']), axis=1)
            doctor_paper_data['keyword_paper'] = doctor_paper_data.apply(
                lambda x: disease_kor_match(x['keyword_paper']), axis=1)
            doctor_paper_data['overlap_paper'] = doctor_paper_data.apply(
                lambda x: overlap_paper(x['paper_disease_all']), axis=1)
            doctor_paper_data['total_paper'] = doctor_paper_data.apply(
                lambda x: (x['paper_impact']*w1+x['cosine_simil_paper']*w2)/(w1+w2), axis=1)

            return doctor_paper_data

        def clinical_score(input):

            doctor_disease_data = pd.DataFrame({'chief_name': doctor_totaldisease['name_kor'],
                                                'belong': doctor_totaldisease['belong'],
                                                'clinical_count': doctor_totaldisease['clinical_count'],
                                                'clinical_disease_all': doctor_totaldisease['clinical_disease_all']
                                                })

            def preprocess(text):

                text = text.replace('.', "dot")
                return text

            target_input = preprocess(input)
            target_name = list(doctor_disease_data['chief_name'])
            target_index = len(target_name)
            target_name.append('target')

            text = list(doctor_disease_data['clinical_disease_all'])
            target_text = [preprocess(t) for t in text]
            target_text.append(target_input)

            doctors = pd.DataFrame({'name': target_name,
                                    'text': target_text})

            tfidf_vector = TfidfVectorizer(min_df=3, max_features=6000)
            tfidf_matrix = tfidf_vector.fit_transform(
                doctors['text']).toarray()

            cosine_sim = cosine_similarity(tfidf_matrix)
            cosine_sim_df = pd.DataFrame(cosine_sim, columns=doctors.name)
            cosine_sim_df.head()

            doctor_disease_data['total_clinical'] = cosine_sim_df['target'][:target_index]

            std = input.split(', ')

            def overlap_clinical(text):
                clinical_overlap = 0
                clinicals = text.split('/ ')
                for clinical in clinicals:
                    clinical = clinical.split(', ')
                    if all(temp in clinical for temp in std):
                        clinical_overlap += 1

                return clinical_overlap

            def overlap_keyword(text):
                text = text.replace('/ ', ', ')
                words = text.split(', ')
                word_target = set(words)
                add_keyword = set(std) & word_target

                words_count = {}
                for word in words:
                    if word in words_count:
                        words_count[word] += 1
                    else:
                        words_count[word] = 1

                sorted_words = sorted(
                    [(k, v) for k, v in words_count.items()], key=lambda word_count: -word_count[1])
                keyword = [w for w in sorted_words if w[0] in add_keyword]
                if(len(keyword) >= 5):
                    keyword = keyword[0:5]

                return keyword

            def disease_kor_match(text):

                for idx in range(0, len(text)):
                    name_kor = disease_match(text[idx][0])
                    if len(name_kor):
                        name_kor = name_kor[text[idx][0]]
                        text[idx] = [text[idx][0], name_kor, text[idx][1]]

                return text

            doctor_disease_data['keyword_clinical'] = doctor_disease_data.apply(
                lambda x: overlap_keyword(x['clinical_disease_all']), axis=1)
            doctor_disease_data['keyword_clinical'] = doctor_disease_data.apply(
                lambda x: disease_kor_match(x['keyword_clinical']), axis=1)
            doctor_disease_data['overlap_clinical'] = doctor_disease_data.apply(
                lambda x: overlap_clinical(x['clinical_disease_all']), axis=1)
            doctor_disease_data['index'] = range(target_index)

            result = doctor_disease_data[[
                'total_clinical', 'overlap_clinical', 'keyword_clinical']]

            return result

        def get_recommendation(input, weight_paper, weight_trial, weight_paper_impact, weight_sim):

            print('추출(검색)된 질병 : ', end=' ')
            print('추출된 질병 (한글명 매칭): ', end=' ')
            print(disease_match(input))

            paper_grade = paper_score(input, weight_paper_impact, weight_sim)
            clinical_grade = clinical_score(input)

            person_grade = pd.concat([paper_grade, clinical_grade], axis=1)

            person_grade['total_score'] = person_grade.apply(lambda x: (
                x['total_paper']*weight_paper + x['total_clinical']*weight_trial)/(weight_paper+weight_trial), axis=1)
            ranking = person_grade.sort_values(
                by='total_score', ascending=False)[0:10]
            ranking['ranking'] = range(1, 11)
            ranking['cosine_simil_paper'] = round(
                ranking['cosine_simil_paper'], 2)
            ranking['total_clinical'] = round(ranking['total_clinical'], 2)
            ranking['total_score'] = round(ranking['total_score'], 2)
            ranking['paper_impact'] = round(ranking['paper_impact'], 2)
            temp = ranking.to_json(orient='records')

            return temp

        return Response(get_recommendation(input, weight_paper, weight_trial, weight_paper_impact=3, weight_sim=7))


class Recommend2API(APIView):

    def get(self, request):
        input = request.GET.get('input', 'I20.2')
        weight_paper = request.GET.get('weight_paper', 7)
        weight_trial = request.GET.get('weight_trial', 3)

        weight_paper = int(weight_paper)
        weight_trial = int(weight_trial)

        dataset = pd.DataFrame(list(DoctorTotalDisease.objects.all().values()))
        disease_table = pd.DataFrame(list(Totaldisease.objects.all().values()))
        dataset = dataset.fillna("")

        df = pd.DataFrame(list(DoctorAllscore.objects.all().values()))

        def disease_match(text):
            text = text.split(', ')
            result = dict()

            for word in text:
                disease_indexs = disease_table[disease_table['disease_code'] == word].index
                if(len(disease_indexs)):
                    result[word] = disease_table['disease_kor'][disease_indexs[0]]
            return result

        def paper_score(input):

            doctor_paper_data = dataset.copy()

            def preprocess(text):
                text = text.replace('.', "dot")
                return text

            def overlap_paper(text):
                paper_overlap = 0
                papers = text.split('/ ')
                for paper in papers:
                    paper = paper.split(', ')
                    if all(temp in paper for temp in std):
                        paper_overlap += 1
                return paper_overlap

            def overlap_keyword(text):
                words_count = {}
                text = text.replace('/ ', ', ')
                words = text.split(', ')
                word_target = set(words)
                add_keyword = set(std) & word_target

                for word in words:
                    if word in words_count:
                        words_count[word] += 1
                    else:
                        words_count[word] = 1

                sorted_words = sorted(
                    [(k, v) for k, v in words_count.items()], key=lambda word_count: -word_count[1])
                keyword = [w for w in sorted_words if w[0] in add_keyword]
                if(len(keyword) >= 5):
                    keyword = keyword[0:5]
                return keyword

            def disease_kor_match(text):
                for idx in range(0, len(text)):
                    name_kor = disease_match(text[idx][0])
                    if(len(name_kor) != 0):
                        name_kor = name_kor[text[idx][0]]
                    else:
                        name_kor = 'x'
                    text[idx] = [text[idx][0], name_kor, text[idx][1]]
                return text

            def simil_large(text):
                target_input = text
                target_name = list(doctor_paper_data['name_kor'])
                target_index = len(target_name)
                target_name.append('target')

                text = list(doctor_paper_data['paper_disease_all'])
                target_text = [preprocess(t) for t in text]
                target_text.append(target_input)

                doctors = pd.DataFrame({'name': target_name,
                                        'text': target_text})

                tfidf_vector = TfidfVectorizer(min_df=3, max_features=6000)
                tfidf_matrix = tfidf_vector.fit_transform(
                    doctors['text']).toarray()

                cosine_sim = cosine_similarity(tfidf_matrix)
                cosine_sim_df = pd.DataFrame(cosine_sim, columns=doctors.name)
                cosine_sim_df.head()

                temp = cosine_sim_df['target'][0:target_index]
                doctor_paper_data['cosine_simil_paper_large'] = temp

                return doctor_paper_data['cosine_simil_paper_large']

            simil_large(input)

            target_input = preprocess(input)
            target_name = list(doctor_paper_data['name_kor'])
            target_index = len(target_name)
            target_name.append('target')

            text = list(doctor_paper_data['paper_disease_all'])
            target_text = [preprocess(t) for t in text]
            target_text.append(target_input)

            doctors = pd.DataFrame({'name': target_name, 'text': target_text})

            tfidf_vector = TfidfVectorizer(min_df=3, max_features=6000)
            tfidf_matrix = tfidf_vector.fit_transform(
                doctors['text']).toarray()

            cosine_sim = cosine_similarity(tfidf_matrix)
            cosine_sim_df = pd.DataFrame(cosine_sim, columns=doctors.name)
            cosine_sim_df.head()

            temp = cosine_sim_df['target'][0:target_index]
            doctor_paper_data['cosine_simil_paper'] = temp

            std = input.split(', ')

            doctor_paper_data['keyword_paper'] = doctor_paper_data.apply(
                lambda x: overlap_keyword(x['paper_disease_all']), axis=1)
            doctor_paper_data['keyword_paper'] = doctor_paper_data.apply(
                lambda x: disease_kor_match(x['keyword_paper']), axis=1)
            doctor_paper_data['overlap_paper'] = doctor_paper_data.apply(
                lambda x: overlap_paper(x['paper_disease_all']), axis=1)
            doctor_paper_data['cosine_simul_paper'] = doctor_paper_data.apply(lambda x: (
                x['cosine_simil_paper']*0.7+x['cosine_simil_paper_large']*0.3), axis=1)

            return doctor_paper_data

        def clinical_score(input):

            doctor_disease_data = pd.DataFrame({'chief_name': dataset['name_kor'],
                                                'belong': dataset['belong'],
                                                'clinical_count': dataset['clinical_count'],
                                                'clinical_disease_all': dataset['clinical_disease_all']
                                                })

            def preprocess(text):
                text = text.replace('.', "dot")
                return text

            def overlap_clinical(text):
                clinical_overlap = 0
                clinicals = text.split('/ ')
                for clinical in clinicals:
                    clinical = clinical.split(', ')
                    if all(temp in clinical for temp in std):
                        clinical_overlap += 1

                return clinical_overlap

            def overlap_keyword(text):
                text = text.replace('/ ', ', ')
                words = text.split(', ')
                word_target = set(words)
                add_keyword = set(std) & word_target

                words_count = {}
                for word in words:
                    if word in words_count:
                        words_count[word] += 1
                    else:
                        words_count[word] = 1

                sorted_words = sorted(
                    [(k, v) for k, v in words_count.items()], key=lambda word_count: -word_count[1])
                keyword = [w for w in sorted_words if w[0] in add_keyword]
                if(len(keyword) >= 5):
                    keyword = keyword[0:5]

                return keyword

            def disease_kor_match(text):
                for idx in range(0, len(text)):
                    name_kor = disease_match(text[idx][0])
                    if len(name_kor):
                        name_kor = name_kor[text[idx][0]]
                        text[idx] = [text[idx][0], name_kor, text[idx][1]]

                return text

            def simil_large(text):
                target_input = text
                target_name = list(doctor_disease_data['chief_name'])
                target_index = len(target_name)
                target_name.append('target')

                text = list(doctor_disease_data['clinical_disease_all'])
                target_text = [preprocess(t) for t in text]
                target_text.append(target_input)

                doctors = pd.DataFrame(
                    {'name': target_name, 'text': target_text})

                tfidf_vector = TfidfVectorizer(min_df=3, max_features=6000)
                tfidf_matrix = tfidf_vector.fit_transform(
                    doctors['text']).toarray()

                cosine_sim = cosine_similarity(tfidf_matrix)
                cosine_sim_df = pd.DataFrame(cosine_sim, columns=doctors.name)
                cosine_sim_df.head()

                doctor_disease_data['cosine_simil_clinical_large'] = cosine_sim_df['target'][:target_index]

                return doctor_disease_data['cosine_simil_clinical_large']

            simil_large(input)

            target_input = preprocess(input)
            target_name = list(doctor_disease_data['chief_name'])
            target_index = len(target_name)
            target_name.append('target')

            text = list(doctor_disease_data['clinical_disease_all'])
            target_text = [preprocess(t) for t in text]
            target_text.append(target_input)

            doctors = pd.DataFrame({'name': target_name, 'text': target_text})

            tfidf_vector = TfidfVectorizer(min_df=3, max_features=6000)
            tfidf_matrix = tfidf_vector.fit_transform(
                doctors['text']).toarray()

            cosine_sim = cosine_similarity(tfidf_matrix)
            cosine_sim_df = pd.DataFrame(cosine_sim, columns=doctors.name)
            cosine_sim_df.head()

            doctor_disease_data['cosine_simil_clinical'] = cosine_sim_df['target'][:target_index]

            std = input.split(', ')

            doctor_disease_data['keyword_clinical'] = doctor_disease_data.apply(
                lambda x: overlap_keyword(x['clinical_disease_all']), axis=1)
            doctor_disease_data['keyword_clinical'] = doctor_disease_data.apply(
                lambda x: disease_kor_match(x['keyword_clinical']), axis=1)
            doctor_disease_data['overlap_clinical'] = doctor_disease_data.apply(
                lambda x: overlap_clinical(x['clinical_disease_all']), axis=1)
            doctor_disease_data['total_clinical'] = doctor_disease_data.apply(lambda x: (
                x['cosine_simil_clinical']*0.7+x['cosine_simil_clinical_large']*0.3), axis=1)
            doctor_disease_data['index'] = range(target_index)
            result = doctor_disease_data[[
                'total_clinical', 'overlap_clinical', 'keyword_clinical']]

            return result

        def get_recommendation(input, weight_paper, weight_trial):
            def calcul_sim(x, y):
                if x[0] == 'p':
                    weight = float(weight_paper/(weight_paper+weight_trial))
                else:
                    weight = float(weight_trial/(weight_paper+weight_trial))
                x = x[2:]
                similarity = 0.0
                if(x == y):
                    similarity += 1
                if x.split('.')[0] == y.split('.')[0]:
                    similarity += 0.01
                if x[0] == y[0]:
                    similarity += 0.0001
                return similarity*weight*100
            print('추출(검색)된 질병 : ', end=' ')
            print('추출된 질병 (한글명 매칭): ', end=' ')
            print(disease_match(input))
            print(weight_paper)
            print(weight_trial)

            paper_grade = paper_score(input)
            clinical_grade = clinical_score(input)
            
            person_grade = pd.concat([paper_grade, clinical_grade], axis=1)
            
            person_grade['total_score'] = person_grade.apply(lambda x: (
                x['cosine_simil_paper']*weight_paper + x['total_clinical']*weight_trial)/(weight_paper+weight_trial), axis=1)
            df['total_score']=""
            for i in df.index:
                total_score = 0.0
                codes = eval(df['disease'][i])
                for code in codes:
                    # 논문/임상시험 가중치 계산
                    sim = calcul_sim(code, input)
                    temp = sim*codes[code]
                    total_score += temp
                df['total_score'][i] = total_score

            sorted_df = df.sort_values(
                by=['total_score'], axis=0, ascending=False)
            sorted_df = sorted_df.reset_index()

            for i in sorted_df.index:
                dic = eval(sorted_df['disease'][i])
                delete = []
                for j in dic:
                    if dic[j] == 0:
                        t = 0
                    else:
                        t = float(dic[j]) * float(calcul_sim(j, input))
                    dic[j] = round(t, 2)
                    if(t == 0.0):
                        delete.append(j)
                for j in delete:
                    del dic[j]
                sdic = sorted(
                    dic.items(), key=lambda x: x[1], reverse=True)[0:5]
                codess = ", ".join([str(_) for _ in sdic])

                # 임시
                belong_name = sorted_df['belong_name'][i]
                belong = sorted_df['belong_name'][i].split('병원')[0] + "병원"
                name = sorted_df['belong_name'][i].split('병원')[1]

                person_grade['major'][i] = codess
                person_grade['belong'][i] = belong
                person_grade['name_kor'][i] = name
                person_grade['total_score'][i] = sorted_df['total_score'][i]

            ranking = person_grade.sort_values(
                by='total_score', ascending=False)[0:10]
            ranking['cosine_simil_paper'] = 0
            ranking['total_clinical'] = 0
            ranking['paper_impact'] = 0
            ranking['total_score'] = round(ranking['total_score'], 2)

            ranking['ranking'] = range(1, 11)
            temp = ranking.to_json(orient='records')

            return temp

        return Response(get_recommendation(input, weight_paper, weight_trial))


class CountAPI(APIView):

    def get(self, request):

        diseases = request.GET.get('input', "I20.1")
        diseases = diseases.split(', ')

        q1 = Q()
        q2 = Q()
        q3 = Q()
        q4 = Q()
        if diseases:
            for disease in diseases:
                q1 &= Q(paper_disease_all__icontains=disease)
                q2 &= Q(clinical_disease_all__icontains=disease)
                q3 |= Q(paper_disease_all__icontains=disease)
                q4 |= Q(clinical_disease_all__icontains=disease)

        q1 |= q2
        q3 |= q4
        queryset1 = DoctorTotalDisease.objects.filter(q1)
        queryset2 = DoctorTotalDisease.objects.filter(q3)
        overall_count = queryset1.count()
        partition_count = queryset2.count()

        result = {'overall_count': overall_count,
                  'partition_count': partition_count}

        return Response(json.dumps(result))


class DiseaseMatchAPI(APIView):

    def get(self, request):

        diseases = request.GET.get('input', "I20.1")
        diseases = diseases.split(', ')

        diseasecode_disease = pd.DataFrame(
            list(Totaldisease.objects.all().values()))

        result = dict()
        for word in diseases:
            disease_indexs = diseasecode_disease[diseasecode_disease['disease_code'] == word].index
            if(len(disease_indexs)):
                result[word] = diseasecode_disease['disease_kor'][disease_indexs[0]]
            else:
                result[word] = "한글 질병명 x"

        return Response(json.dumps(result))


class ExtractDieaseAPI(APIView):

    def get(self, request):

        client = boto3.client(
            service_name=get_secret('service_name'),
            region_name=get_secret('region_name'),
            aws_access_key_id=get_secret('aws_access_key_id'),
            aws_secret_access_key=get_secret('aws_secret_access_key'),
        )

        # API 호출
        text = request.GET.get('summary', "")
        resp = client.infer_icd10_cm(Text=text)

        data = resp
        for i, values in enumerate(data.values()):
            if i == 0:
                df2 = pd.DataFrame(values)

        try:
            df = df2[['ICD10CMConcepts']]
            # print(df)
        except:
            pass

        disease_code = []
        for k, v in enumerate(df['ICD10CMConcepts']):
            if v != []:
                d = []
                for i, j in enumerate(v):
                    d.append(j)
                # print(d)

                df1 = pd.DataFrame(d)
                # print(df1)
                disease_codes = list(df1['Code'])  # ACM으로 분석된 질병코드
                disease_code += disease_codes
        # print(Counter(disease_code))

        freq_list = sorted(
            disease_code, key=lambda x: (-disease_code.count(x), disease_code.index(x)))
        # print(freq_list)

        temp = list(dict.fromkeys(freq_list))
        # print(temp)
        code_list = []

        for i in temp:
            cnt = 0
            for l in freq_list:
                if i == l:
                    cnt += 1
            code_list.append(i + '(' + str(cnt) + ')')
            result = code_list

        return Response(json.dumps(result))