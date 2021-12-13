<template>
  <section class = 'ma-10' >

    <div class="overflow-hidden pa-5 ma-5 d-flex justify-start">

      <v-row>
        <v-col cols='6'>

            <v-text-field
              label="질병코드를 (, ) 로 구분해서 입력하세요. [ 예시: I21.9, Q23 ]"
              hint="질병코드를 (, ) 로 구분해서 입력하세요. [ 예시: I21.9, Q23 ]"
              persistent-hint
              rounded
              outlined
              solo
              @keyup.enter = "re2"
              v-model=input
            >
            </v-text-field>
          </v-col>

          <v-col cols='1' >
            
            <v-btn
              class = 'ma-3'
              color="light-blue lighten-2"
              @click="detail_search = !detail_search"
            >
              상세 검색
            </v-btn>
            
        </v-col> 
      </v-row>   

    </div>
    
    <div class='d-flex  flex-wrap'>
      <div class="d-flex flex-wrap">
        <span><strong>질병명: </strong></span>
        <span v-bind:key='key' v-for="(value, key) in diseasematch" > 
          <strong class="px-2 text-center blue lighten-3 rounded-xl mx-2">{{key}} - {{value}}</strong>
        </span>
      </div>

      <div class="d-flex align-start flex-wrap mb-6 ml-auto">
          <v-btn
            rounded
            :color=color
            dark
            @click = chageapi
          >
            추천 {{click}}
          </v-btn>
      </div>
    </div>


   
    <v-btn
      fab
      color="cyan accent-2"
      right
      absolute
      @click="dialog = !dialog"
    >
      <v-icon> mdi-comment-question </v-icon>
    </v-btn>

    <v-dialog
      v-model="dialog"
      max-width="700px"
    >
      <v-card>
        <v-card-title>추천 로직</v-card-title>

        <v-card-text>
          <p> 의료진의 저명성: 논문 impact = citation값과 논문이 등재된 저널의 jci 값을 다 더한 후 정규화한 값</p>
          <p> 의료진의 질병분야 전문성: 검색 질병명과 의료진이 쓴 논문, 임상시험 관련 질병명 간의 코사인 유사도를 구한 값</p>
          <v-spacer></v-spacer>
          <p>전체 점수 = 논문 점수*0.7 + 임상시험 질병 유사도 점수*0.3 </p>
          <p>논문 점수 = 논문 질병 유사도 점수*0.7 + 논문 impact*0.3</p>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            text
            color="primary"
            @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="detail_search"
      max-width="900px"
      width='900px'
    >
      <v-card>
        
        <div class= 'pa-6 ma-5'>
          <h3 class="font-weight-black"> 임상시험명 </h3>
          <v-text-field
            :rules="rules"
            hide-details="auto"
            v-model='title'
          ></v-text-field>
          

          <h3 class ="font-weight-black text-align-left mt-4"> Brief Summary </h3>
          <v-textarea
            :rules="rules"
            v-model="summary"
            auto-grow
            filled
            color="deep-purple"
            rows="4"
            class = 'my-5'
          ></v-textarea>
       
          <v-spacer></v-spacer>

          <v-btn
            
            color="primary"
            @click="getSummaryInput"
            class ="font-weight-black"
          >
            Submit
          </v-btn>
        </div>

        <v-item-group multiple
        v-if = "showextractdisease">
          <v-subheader>추출된 질병명</v-subheader>

            <v-item
              v-for="( item, i ) in extractdisease"
              :key="i"
              class='pa-3 ma-3'
              v-slot="{ active, toggle }"
            >
              <v-chip
                active-class="purple--text"
                :input-value="active"
                @click="[toggle(), updateDiseaseSet(active, item)]"             
              >

                {{item}}
              </v-chip>
            </v-item>
        </v-item-group>

        <v-btn
            v-if = "showextractdisease"
            color="primary"
            @click="readyforRecommend"
            class ="font-weight-black mb-5"
          >
            추천
          </v-btn>
        
      </v-card>
    </v-dialog>

    <v-data-table
      :headers="headers"
      :items="items"
      hide-default-footer
      class="elevation-1"
    >

      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>
            검색 결과 <span class="text-no-wrap light-blue lighten-4">{{partition_count}}</span>명의 의료진이
            있습니다.
          </v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>

    <template v-slot:header>
      <thead>
         <tr> 
          <th colspan="5" scope="colgroup">추천 결과</th> 
          </tr> 
          <tr>
          <th colspan="5" ></th>
          <th colspan="2"> <p class="text-center">질병 전문성</p></th>
          <th scope="col"> <p class="text-center">저명성</p></th>
          <th colspan="2"> <p class="text-center">활동성</p></th> 
        </tr> 
      </thead>
    </template>

      <template v-slot:[`item.img`] ="{ item }">

          <img :src="item.img" />
      </template>


      <template v-slot:[`item.name_kor`] ="{ item }">

          {{ item.name_kor }}
          <v-spacer></v-spacer>
          {{ item.belong }}

      </template>

      <template v-slot:[`item.total_clinical`] ="{ item }">

          {{ item.total_clinical }}
          <v-spacer></v-spacer>
          ({{ item.overlap_clinical}}<span>건</span>)

      </template>

      <template v-slot:[`item.cosine_simil_paper`] ="{ item }">

          {{ item.cosine_simil_paper }}
          <v-spacer></v-spacer>
          ({{ item.overlap_paper}}<span>건</span>)

      </template>

      <template v-slot:[`item.paper_count`] ="{ item }">

          {{ item.paper_count }}<span>건</span>

      </template>

      <template v-slot:[`item.clinical_count`] ="{ item }">

          {{ item.clinical_count }} 
          <span>건</span>

      </template>

    </v-data-table>

  </section>
</template>

<script>
import api from '../api';


export default {
        data(){
            return{
            title: "",
            showextractdisease: false,
            extractdisease : ['I20.1', 'I21.9', 'I55.9'],
            summary: "",
            toggle: false,
            color: 'primary',
            click: 'A',
            previous:'I20.1',
            target: [],
            rules: [
                    value => !!value || 'Required.',
                    value => (value && value.length >= 3) || 'Min 3 characters',
                  ],
            dialog: false,
            detail_search: false,
            overall_count: 0,
            partition_count: 0,
            diseasematch: {},
            value: 1,
            active: false,
            input : "I20.1",
            items : [],
            groupBy: [],
            groupDesc: [],
            headers: [
            { text: '추천순', value: 'ranking'},
            { text: '', value: 'img'},
            {
              text: 'Totalscore', value: 'total_score',
            },
            { text: 'Name', value: 'name_kor' , sortable: false, },
            { text: 'Major', value: 'major' , sortable: false,},
            { text: '논문', value: 'cosine_simil_paper'},
            { text: '임상시험', value: 'total_clinical' },           
            { text: 'paper_impact', value: 'paper_impact' },
            { text: '전체 논문 수', value: 'paper_count' },
            { text: '전체 임상 수', value: 'clinical_count' },
                     
        ],
           
            };
        },
        watch: {

    },

 methods: {
   getSummaryInput(){
     
     this.showextractdisease = true
     this.getExtractDiseaseResults()

   },
   updateDiseaseSet(active, item){
     if(active === true){
       for(let i = 0; i < this.target.length; i++) {
        if(this.target[i] === item){
          this.target.splice(i, 1);
        }
      }
     }
     else{
       this.target.push(item)
     }
     
   },
   readyforRecommend(){
     this.showextractdisease = false
     this.detail_search = false
     this.summary = ""
     this.title = ""
     this.input = this.target.join(', ')
     this.target = []
     this.re2()
   },
   chageapi(){
     this.toggle = !this.toggle
    
     if(this.toggle === true){
       this.color = 'cyan accent-6'
       this.click = 'B'
       this.input = this.previous
       this.getRecommendResults2()     
     }
     else{
       this.color = 'primary'
       this.click = 'A'
       this.input = this.previous
       this.getRecommendResults()
     }
      this.getCountResults()
      this.getDiseaseMatchResults() 
     this.input= ""
   },
    re2() {
      
      this.getRecommendResults();
      this.getCountResults();
      this.getDiseaseMatchResults();
      this.toggle = false;
      this.color = 'primary'
      this.click = 'A'
      this.previous = this.input;
      this.input= ""
    },
    async getRecommendResults () {
      
      try {
         const temp = this.input
        
        const params = {
          input : temp,
        }
        
        const res = await api.recommend(params)
        this.items = res['data']
        this.items = JSON.parse(this.items)

      } catch (err) {
        console.log(err)
      }

    },
    async getRecommendResults2 () {
      
      try {
         const temp = this.input
        
        const params = {
          input : temp,
        }
        
        const res = await api.recommend2(params)
        
        this.items = res['data']
        this.items = JSON.parse(this.items)
  

      } catch (err) {
        console.log(err)
      }

    },
    async getCountResults () {
    
      try {
          const temp = this.input
          
        const params = {
          input : temp,
        }
        
        const res = await api.getCount(params)
        
        let result = res['data']
        result = JSON.parse(result)
        this.overall_count = result['overall_count']
        this.partition_count = result['partition_count']
        

      } catch (err) {
        console.log(err)
      }
    },
    async getDiseaseMatchResults () {
    
      try {
          const temp = this.input
        const params = {
          input : temp,
        }
        const res = await api.getDiseaseMatch(params)
        let result = res['data']
        this.diseasematch = JSON.parse(result)

      } catch (err) {
        console.log(err)
      }
    },
    async getExtractDiseaseResults() {
    
      try {
          const temp = this.summary
        const params = {
          input : temp,
        }
        const res = await api.getExtractDisease(params)
        let result = res['data']
        this.extractdisease = JSON.parse(result)

      } catch (err) {
        console.log(err)
      }
    },
    
    
 },


mounted: function () {
    this.input = this.$route.params.disease;
    if(this.input === '') this.input = "I20.1";
    this.previous = this.input;
    this.re2()
    
  },
       
};

</script>



<style>

@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

section {
  font-family: 'Nanum Gothic', sans-serif;
}

img {
  width: 4rem;
  height: 4rem;
  object-fit: cover;
  border-radius: 70%;
  padding: 0.5rem;
}

</style>