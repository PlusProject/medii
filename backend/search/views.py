from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import ClinicalTrials, Disease, Person, Participate, Writes, Thesis, DoctorTotalDisease, Totaldisease, DoctorAllscore, SnPaper, SnPaperCnt,NodeCris,NodeCrisCnt, SnPaper50, SnPaperCnt50, DoctorAll, DoctorAll2,DoctorAll3,PartPaperNode,PartPaperEdge,SnPaperEdgeYear
from .serializers import (ClinicalTrialsSerializer, HospitalSerializer, ThesisSerializer, NameSerializer,
                          PersonSerializer, ParticipateSerializer, WritesSerializer,
                          CrisCoworkerSerializer, ThesisCoworkerSerializer, DiseaseSerializer, DiseaseSerializer, DoctorTotalDiseaseSerializer, Totaldisease, DoctorAllscoreSerializer,
                          SnPaperSerializer,SnPaperCntSerializer,NodeCrisSerializer,NodeCrisCntSerializer,SnPaper50Serializer,SnPaperCnt50Serializer,DoctorAllSerializer,DoctorAll2Serializer,DoctorAll3Serializer
                          ,PartPaperNodeSerializer,PartPaperEdgeSerializer,SnPaperEdgeYearSerializer)
from django.db.models import Q
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import minmax_scale
import json
from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
import boto3
import time
import warnings
warnings.filterwarnings(action='ignore')

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
def partpapernode_view(request):
    partpapernode=PartPaperNode.objects.all()
    return Response(PartPaperNodeSerializer(partpapernode, many=True).data)

@api_view(['GET'])
def partpaperedge_view(request):
    partpaperedge=PartPaperEdge.objects.all()
    return Response(PartPaperEdgeSerializer(partpaperedge, many=True).data)

@api_view(['GET'])
def snpaperedgeyear_view(request):
    snpaperedgeyear=SnPaperEdgeYear.objects.all()
    return Response(SnPaperEdgeYearSerializer(snpaperedgeyear, many=True).data)


@api_view(['GET'])
def snpaper_view(request):
    snpapers=SnPaper.objects.all()
    return Response(SnPaperSerializer(snpapers, many=True).data)

@api_view(['GET'])
def snpapercnt_view(request):
    snpapercnts=SnPaperCnt.objects.all()
    return Response(SnPaperCntSerializer(snpapercnts, many=True).data)

@api_view(['GET'])
def nodecris_view(request):
    nodecriss=NodeCris.objects.all()
    return Response(NodeCrisSerializer(nodecriss, many=True).data)

@api_view(['GET'])
def nodecriscnt_view(request):
    nodecriscnts=NodeCrisCnt.objects.all()
    return Response(NodeCrisCntSerializer(nodecriscnts, many=True).data)

@api_view(['GET'])
def snpaper50_view(request):
    snpapers50=SnPaper50.objects.all()
    return Response(SnPaper50Serializer(snpapers50, many=True).data)

@api_view(['GET'])
def snpapercnt50_view(request):
    snpapercnts50=SnPaperCnt50.objects.all()
    return Response(SnPaperCnt50Serializer(snpapercnts50, many=True).data)
    
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


class Recommend2API(APIView):

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
            doctor_paper_data['o_p'] = temp

            doctor_paper_data['keyword_paper'] = doctor_paper_data.apply(
                lambda x: overlap_keyword(x['paper_disease_all']), axis=1)
            doctor_paper_data['keyword_paper'] = doctor_paper_data.apply(
                lambda x: disease_kor_match(x['keyword_paper']), axis=1)
            doctor_paper_data['overlap_paper'] = doctor_paper_data.apply(
                lambda x: overlap_paper(x['paper_disease_all']), axis=1)
            doctor_paper_data['total_paper'] = doctor_paper_data.apply(
                lambda x: (x['paper_impact']*w1+x['o_p']*w2)/(w1+w2), axis=1)

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

            doctor_disease_data['o_c'] = cosine_sim_df['target'][:target_index]

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
                'o_c', 'overlap_clinical', 'keyword_clinical']]

            return result

        def get_recommendation(input, weight_paper, weight_trial, weight_paper_impact, weight_sim):

            print('추출(검색)된 질병 : ', end=' ')
            print('추출된 질병 (한글명 매칭): ', end=' ')
            print(disease_match(input))

            paper_grade = paper_score(input, weight_paper_impact, weight_sim)
            clinical_grade = clinical_score(input)

            person_grade = pd.concat([paper_grade, clinical_grade], axis=1)

            person_grade['total_score'] = person_grade.apply(lambda x: (
                x['total_paper']*weight_paper + x['o_c']*weight_trial)/(weight_paper+weight_trial), axis=1)
            ranking = person_grade.sort_values(
                by='total_score', ascending=False)[0:20]
            ranking['ranking'] = range(1, 21)
            ranking['o_p'] = round(ranking['o_p'], 2)
            ranking['o_c'] = round(ranking['o_c'], 2)
            ranking['total_score'] = round(ranking['total_score'], 2)
            ranking['paper_impact'] = round(ranking['paper_impact'], 2)
            ranking['top1'] = ranking['major']
            temp = ranking.to_json(orient='records')
            return temp

        return Response(get_recommendation(input, weight_paper, weight_trial, weight_paper_impact=3, weight_sim=7))


class RecommendAPI(APIView):
    def get(self, request):
        time1 = time.time()
        input = request.GET.get('input', 'I20.2')
        weight_paper = request.GET.get('weight_paper', 7)
        weight_trial = request.GET.get('weight_trial', 3)

        weight_paper = int(weight_paper)
        weight_trial = int(weight_trial)

        df = pd.DataFrame(list(DoctorAll2.objects.all().values()))
        disease_table = pd.DataFrame(list(Totaldisease.objects.all().values()))
        input_codes = input.split(', ')
        
        # 불필요한 칼럼 삭제
        big_codes = []
        for input_code in input_codes:
            big_codes.append((input_code[0]).lower())
        for i in range(ord('a'),ord('z')+1):
            if chr(i) not in big_codes:
                df.drop(chr(i), inplace=True, axis=1)

        def disease_match(text):
            text = text.split(', ')
            result = dict()
            for word in text:
                disease_indexs = disease_table[disease_table['disease_code'] == word].index
                if(len(disease_indexs)):
                    result[word] = disease_table['disease_kor'][disease_indexs[0]]
            return result
        
        def disease_match_one(text):
            disease_indexs = disease_table[disease_table['disease_code'] == text].index
            if(len(disease_indexs)):
                return " {" + disease_table['disease_kor'][disease_indexs[0]] + "} "
            else:
                return " {-} "
            
        # 새로운 추천 알고리즘
        def get_recommendation(input, weight_paper, weight_trial):
            def overlap(text):
                overlap = 0
                clinicals = text.split('/ ')
                for clinical in clinicals:
                    clinical = clinical.split(', ')
                    if all(temp in clinical for temp in input_codes):
                        overlap += 1
                return overlap
            
            def overlap2(text):
                if text=="":
                    return 0
                count = 0
                dic = eval(text)
                input_code = "\'"+input.split('.')[0]
                for i in dic:
                    if  input_code==i.split('.')[0]:
                        count+=1
                return count

            def calcul_sim(x, y):
                x = x[2:]
                if(x == y):
                    return 100
                if x.split('.')[0] == y.split('.')[0]:
                    return 10
                if x[0] == y[0]:
                    return 0.01
                return 0
            
            print('추출된 질병 (한글명 매칭): ', end=' ')
            print(disease_match(input))
            df['o_p'] = 0.0
            df['real_o_p'] = 0.0
            df['o_c'] = 0.0
            df['real_o_c'] = 0.0
            df['top1'] = ""
            df['top2'] = ""
            df['top3'] = ""
            df['explain1'] = ""
            df['explain2'] = ""
            df['explain3'] = ""
            df['explainp'] = ""
            df['explainc'] = ""
            df['paper_count'] = df['paper_count'].fillna(0)
            df['clinical_count'] = df['clinical_count'].fillna(0)
            df['paper_impact'] = df['paper_impact'].fillna(0.0)
            df['paper_disease_all'] = df['paper_disease_all'].fillna("")
            df['clinical_disease_all'] = df['clinical_disease_all'].fillna("")
            df['clinical_allcount'] = df['clinical_allcount'].fillna("")
            df['paper_allcount'] = df['paper_allcount'].fillna("")
            
            time2 = time.time()
            print(str(round(time2-time1,3)) + "초 소요 : 1")
            code_num = len(input_codes)
            for input_code in input_codes:
                for i in df.index:
                    # 대분류 도입
                    input_big = input_code[0].lower()
                    codes = eval(df[input_big][i])
                    ptemp = 0.0
                    ctemp = 0.0
                    # 논문/임상시험 가중치 계산
                    for code in codes: 
                        sim = calcul_sim(code, input_code)
                        temp = sim*codes[code]
                        if code[0]=='p':
                            ptemp+=temp
                        else:
                            ctemp+=temp
                    df['o_c'][i] = ctemp
                    df['o_p'][i] = ptemp
                
                if(code_num>1):
                    # mean_score = df['total_score'].mean()
                    # std_score = df['total_score'].std()
                    # df['total_score'] = (df['total_score']-mean_score)/std_score
                    mean_score = df['o_p'].mean()
                    std_score = df['o_p'].std()
                    df['o_p'] = (df['o_p']-mean_score)/std_score
                    mean_score = df['o_c'].mean()
                    std_score = df['o_c'].std()
                    df['o_c'] = (df['o_c']-mean_score)/std_score
                df['real_o_p'] += df['o_p']
                df['real_o_c'] += df['o_c']
                
            time3 = time.time()
            print(str(round(time3-time2,3)) + "초 소요 : 2")
            
            wp = float(weight_paper)
            wt = float(weight_trial)
            wpt = wp+wt
            df['o_p'] = df['real_o_p']
            df['o_c'] = df['real_o_c']
            
            pmax = df['o_p'].max()
            pmin = df['o_p'].min()
            pweight = 100*wp/((pmax-pmin)*wpt)
            df['o_p'] = df['o_p']-pmin
            df['o_p'] = df['o_p'] * pweight
            
            cmax = df['o_c'].max()
            cmin = df['o_c'].min()
            cweight = 100*wt/((cmax-cmin)*wpt)
            df['o_c'] = df['o_c']-cmin
            df['o_c'] = df['o_c']*cweight
            df['total_score'] = df['o_p'] + df['o_c']
            
            sorted_df = df.sort_values(
                by=['total_score'], axis=0, ascending=False)[0:20]
            sorted_df = sorted_df.reset_index()
            total_total_score = sorted_df['total_score'].sum()
            # 정규화
            tmax = sorted_df['total_score'].max()
            tmin = sorted_df['total_score'].min()
            sorted_df['total_ratio'] = sorted_df['total_score']/total_total_score
            # sorted_df['total_score'] = (sorted_df['total_score'] - tmin)/(tmax-tmin)
            
            print(cweight, pweight)
            # sorted_df['paper_disease_all'] = sorted_df['paper_disease_all'].fillna("")
            # sorted_df['clinical_disease_all'] = sorted_df['clinical_disease_all'].fillna("")
            for i in sorted_df.index:
                dic = eval(sorted_df['disease'][i])
                delete = []
                for j in dic:
                    t=0.0
                    for input_code in input_codes:
                        if j[0]=='p':
                            t += float(dic[j]) * float(calcul_sim(j, input_code)) * pweight
                        else:
                            t += float(dic[j]) * float(calcul_sim(j, input_code)) * cweight
                    dic[j] = round(t, 2)
                    if(t == 0.0): delete.append(j)
                for j in delete: del dic[j]
                sdic = sorted(
                    dic.items(), key=lambda x: x[1], reverse=True)[0:5]
                explain = ""
                for j in sdic:
                    explain += disease_match_one(j[0][2:])
              
                codes = ", ".join([str(_) for _ in sdic]).replace('p-','논문-').replace('t-','임상-')
                codes = codes.replace('\',',':').replace('(','').replace(')','').replace(',',' ')
                codes += explain
                # print(codes + "," + explain)
                # print(codes.split(" "))
                code1 = (codes.split(" ")[0] + " "+ codes.split(" ")[1]).lstrip("\'")+"\n"
                code2 = (codes.split(" ")[3] + " "+ codes.split(" ")[4]).lstrip("\'")+"\n"
                code3 = (codes.split(" ")[6] + " "+ codes.split(" ")[7]).lstrip("\'")+"\n"
                explain1 = (explain.split("} ")[0])+"}"
                explain2 = (explain.split("} ")[1])+"}"
                explain3 = (explain.split("} ")[2])+"}"
                if len(explain1)<5:
                    explain1 = ""
                if len(explain2)<5:
                    explain2 = ""
                if len(explain3)<5:
                    explain3 = ""
                sorted_df['top1'][i] = code1 
                sorted_df['top2'][i] = code2
                sorted_df['top3'][i] = code3
                sorted_df['explain1'][i] = explain1
                sorted_df['explain2'][i] = explain2
                sorted_df['explain3'][i] = explain3
                sorted_df['explainp'][i] = "("+str(overlap2(sorted_df['paper_allcount'][i])) + "건)"
                sorted_df['explainc'][i] = "("+str(overlap2(sorted_df['clinical_allcount'][i]))+ "건)"
                sorted_df['name_kor'][i] = sorted_df['name_kor'][i]
                sorted_df['major'][i] = codes
                sorted_df['o_p'][i] = str(round(sorted_df['o_p'][i],2)) 
                sorted_df['o_c'][i] = str(round(sorted_df['o_c'][i],2)) 
                # sorted_df['total_score'][i] = str(round(sorted_df['total_score'][i],2))  +"\n"+"(" +str(round(sorted_df['total_ratio'][i],2)) +"%)"
                sorted_df['total_score'][i] = str(round(sorted_df['total_score'][i],2))  
                sorted_df['paper_impact'][i] = str(round(float(sorted_df['paper_impact'][i]), 2))
            
            time4 = time.time()
            print(str(round(time4-time3,3)) + "초 소요: 3")
            sorted_df['ranking'] = range(1, 21)           
            # sorted_df['o_p'] = round(sorted_df['o_p'],2)
            # sorted_df['o_c'] = round(sorted_df['o_c'],2)

            temp = sorted_df.to_json(orient='records')
            time5 = time.time()
            print(str(round(time5-time4,3)) + "초 소요: 4")            
            print("총 소요 시간: " + str(round(time5-time1,3)) + "초")            
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
                q1 &= Q(paper_allcount__icontains=disease)
                q2 &= Q(clinical_allcount__icontains=disease)
                q3 |= Q(paper_allcount__icontains=disease)
                q4 |= Q(clinical_allcount__icontains=disease)

        q1 |= q2
        q3 |= q4
        queryset1 = DoctorAll2.objects.filter(q1)
        queryset2 = DoctorAll2.objects.filter(q3)
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