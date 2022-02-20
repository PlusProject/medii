<template>
  <section class="ma-10">
    <div class="overflow-hidden pa-5 ma-5 d-flex justify-start">
      <v-row>
        <v-col cols="6">
          <v-text-field
            label="질병코드를 (, ) 로 구분해서 입력하세요. [ 예시: I21.9, Q23 ]"
            hint="질병코드를 (, ) 로 구분해서 입력하세요. [ 예시: I21.9, Q23 ]"
            persistent-hint
            rounded
            outlined
            solo
            @keyup.enter="re2"
            v-model="input"
          >
          </v-text-field>
        </v-col>

        <v-col cols="1">
          <v-btn
            class="ma-3"
            color="light-blue lighten-2"
            @click="detail_search = !detail_search"
          >
            상세 검색
          </v-btn>
        </v-col>
      </v-row>
    </div>

    <div class="d-flex flex-wrap">
      <div class="d-flex flex-wrap">
        <span><strong>질병명: </strong></span>
        <span v-bind:key="key" v-for="(value, key) in diseasematch">
          <strong class="px-2 text-center blue lighten-3 rounded-xl mx-2"
            >{{ key }} - {{ value }}</strong
          >
        </span>
      </div>
    </div>

    <v-btn fab color="cyan accent-2" right absolute @click="dialog = !dialog">
      <v-icon> mdi-comment-question </v-icon>
    </v-btn>

    <v-dialog v-model="dialog" max-width="850px">
      <v-card class="text-sm-left pa-7">
        <v-card-title>추천 로직</v-card-title>

        <p class="blue lighten-3">기존 추천</p>
        <v-spacer></v-spacer>
        <p>
          의료진의 저명성: 논문 impact = citation값과 논문이 등재된 저널의 jci
          값을 다 더한 후 정규화한 값
        </p>
        <p>
          의료진의 질병분야 전문성: 검색 질병명과 의료진이 쓴 논문, 임상시험
          관련 질병명 간의 코사인 유사도를 구한 값
        </p>
        <v-spacer></v-spacer>
        <p>전체 점수 = 논문 점수*0.7 + 임상시험 질병 유사도 점수*0.3</p>
        <p>논문 점수 = 논문 질병 유사도 점수*0.7 + 논문 impact*0.3</p>
        <v-spacer></v-spacer>
        <p class="blue lighten-3">신규 추천</p>
        <p>
          <v-spacer></v-spacer>
        </p>
        <p>
          □ 크롤링한 논문과 임상시험 정보에서 ACM API를 사용하여 질병 코드 및
          score 추출 후 해당하는 의사에게 점수 부여
        </p>
        <p>□ 의사 별 논문/임상시험 따로 질병 코드 합산 후 DB 저장</p>
        <p>
          □ 사용자로부터 입력 받은 질병코드에 대해 의사별로 전문성
          계산(한국표준질병사인분류에 따른 질병 간 유사도 반영)
        </p>
        <p>□ 입력 받은 논문/임상 가중치에 따라 최종 점수 계산</p>
        <p>□ 최종 점수를 기준으로 정렬하여 의사 추천(상위 20명)</p>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn text color="primary" @click="dialog = false"> Close </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="detail_search" max-width="900px" width="900px">
      <v-card>
        <div class="pa-6 ma-5">
          <h3 class="font-weight-black">임상시험명</h3>
          <v-text-field
            :rules="rules"
            hide-details="auto"
            v-model="title"
          ></v-text-field>

          <h3 class="font-weight-black text-align-left mt-4">Brief Summary</h3>
          <v-textarea
            :rules="rules"
            v-model="summary"
            auto-grow
            filled
            color="deep-purple"
            rows="4"
            class="my-5"
          ></v-textarea>

          <v-spacer></v-spacer>

          <v-btn
            color="primary"
            @click="getSummaryInput"
            class="font-weight-black"
          >
            Submit
          </v-btn>
        </div>

        <v-item-group multiple v-if="showextractdisease">
          <v-subhearder>추출된 질병명 </v-subhearder>
          <v-subheader>
            (추천에 사용될 질병코드를 선택해주세요 선택하지 않으신 경우 모든
            질병 코드가 추천에 사용됩니다)</v-subheader
          >

          <v-item
            v-for="(item, i) in extractdisease"
            :key="i"
            class="pa-3 ma-3"
            v-slot="{ active, toggle }"
          >
            <v-chip
              active-class="purple--text"
              :input-value="active"
              @click="[toggle(), updateDiseaseSet(active, item)]"
            >
              {{ item }}
            </v-chip>
          </v-item>
        </v-item-group>

        <v-btn
          v-if="showextractdisease"
          color="primary"
          @click="readyforRecommend"
          class="font-weight-black mb-5"
        >
          추천
        </v-btn>
      </v-card>
    </v-dialog>

    <v-data-table
      v-model="selected"
      show-select
      :headers="headers"
      :items="items"
      hide-default-footer
      class="elevation-1"
      :loading="loading"
      loading-text="Loading... Please wait"
      :items-per-page="20"
    >

      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>
            검색 결과
            <span class="text-no-wrap light-blue lighten-4">{{
              partition_count
            }}</span
            >명의 의료진이 있습니다.
          </v-toolbar-title>
          <v-spacer></v-spacer>

          <span> 임상시험 가중치 </span>
          <v-slider
            v-model="clinical.val"
            :color="clinical.color"
            thumb-label="always"
            max="10"
          >
            <template v-slot:thumb-label="{ value }">
              {{ satisfactionEmojis[Math.min(Math.floor(value), 10)] }}
            </template></v-slider>
          <span> 논문 가중치 </span>
          <v-btn
            color="light-blue darken-4"
            @click="changeWeight" 
            class="font-weight-black white--text px-3 ma-5"
          >
            가중치 변경
          </v-btn>
          <th colspan="3">
            <v-btn rounded :color="color" dark small @click="chageapi">
              {{ click }} 추천 알고리즘으로 변경 ->
            </v-btn>
          </th>
        </v-toolbar>
      </template>

      <template v-slot:header>
        <thead>
          <!-- <tr>
          <th colspan="1" scope="colgroup"></th>
          </tr> -->

          <tr>
            <th colspan="4">
              <v-btn
                id="network"
                
                class="indigo lighten-3 my-8 mx-1"
                dark
                @click="
                  $router.push({
                    name: 'allnetwork',
                    params: { select: selected, disease: previous },
                  })
                "
              >
                의사 network 보기
              </v-btn>
            </th>

            <th colspan="5"><p class="text-center">질병 전문성</p></th>
            <th colspan="2"><p class="text-center">저명성</p></th>
            <th colspan="3"><p class="text-center">활동성</p></th>
          </tr>
        </thead>
      </template>
      <template v-slot:[`item.checkbox`]>
        <input type="checkbox" name="doc" />
      </template>

      <template v-slot:[`item.img`]="{ item }">
        <img :src="item.img" />
      </template>
      <template v-slot:[`item.name_kor`]="{ item }">
        <a v-if="item.link" :href="item.link" target="_blank"
          >{{ item.name_kor }}
        </a>

        <span v-else>{{ item.name_kor }}</span>
        <v-spacer></v-spacer>
        {{ item.belong }}
      </template>

      <template v-slot:[`item.top1`]="{ item }">
        <span style="font-size: 120%">
          <strong>
            {{ item.top1 }}
          </strong>
        </span>
        <v-spacer></v-spacer>
        {{ item.explain1 }}
      </template>

      <template v-slot:[`item.top2`]="{ item }">
        <span style="font-size: 110%">
          {{ item.top2 }}
        </span>
        <v-spacer></v-spacer>
        {{ item.explain2 }}
      </template>

      <template v-slot:[`item.top3`]="{ item }">
        <span style="font-size: 105%">
          {{ item.top3 }}
        </span>
        <v-spacer></v-spacer>
        {{ item.explain3 }}
      </template>

      <template v-slot:[`item.o_p`]="{ item }">
        {{ item.o_p }}
        <v-spacer></v-spacer>
        {{ item.explainp }}
      </template>

      <template v-slot:[`item.o_c`]="{ item }">
        {{ item.o_c }}
        <v-spacer></v-spacer>
        {{ item.explainc }}
      </template>

      <template v-slot:[`item.total_clinical`]="{ item }">
        {{ item.total_clinical }}
        <v-spacer></v-spacer>
        ({{ item.overlap_clinical }}<span>건</span>)
      </template>

      <template v-slot:[`item.cosine_simil_paper`]="{ item }">
        {{ item.cosine_simil_paper }}
        <v-spacer></v-spacer>
        ({{ item.overlap_paper }}<span>건</span>)
      </template>

      <template v-slot:[`item.paper_count`]="{ item }">
        {{ item.paper_count }}<span>건</span>
      </template>

      <template v-slot:[`item.clinical_count`]="{ item }">
        {{ item.clinical_count }}
        <span>건</span>
      </template>
    </v-data-table>
  </section>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      tmp_info: [],
      clinical: { label: "임상시험 가중치", val: 7, color: "primary darken-3" },
      paper: { label: "논문 가중치", val: 3, color: "blue-grey darken-2" },
      loading: true,
      title: "",
      showextractdisease: false,
      extractdisease: [],
      summary: "",
      toggle: false,
      color: "primary",
      click: "기존 ",
      previous: "I20.1",
      target: [],
      rules: [
        (value) => !!value || "Required.",
        (value) => (value && value.length >= 3) || "Min 3 characters",
      ],
      dialog: false,
      detail_search: false,
      overall_count: 0,
      partition_count: 0,
      diseasematch: {},
      value: 1,
      active: false,
      input: "I20.1",
      items: [],
      previous_items: null,
      previous_items2: null,
      groupBy: [],
      groupDesc: [],
      selected:[],
      headers: [
        { text: "추천순", value: "ranking" },
        { text: "", value: "img" },
        {
          text: "Totalscore",
          value: "total_score",
        },
        { text: "Name", value: "name_kor", sortable: false },
        { text: "Code Top1", value: "top1", sortable: false },
        { text: "Code Top2", value: "top2", sortable: false },
        { text: "Code Top3", value: "top3", sortable: false },
        // { text: "Major", value: "major", sortable: false },
        { text: "논문", value: "o_p" },
        { text: "임상시험", value: "o_c" },
        { text: "paper_impact", value: "paper_impact" },
        { text: "전체 논문 수", value: "paper_count" },
        { text: "전체 임상 수", value: "clinical_count" },
      ],
      satisfactionEmojis: ['0:10', '1:9', '2:8', '3:7', '4:6', '5:5', '6:4', '7:3', '8:2', '9:1','10:0'],
        
    };
  },

  watch: {},

  methods: {
    selectAll(selectAll) {
      const checkboxes = document.getElementsByName("doc");
      checkboxes.forEach((checkbox) => {
        checkbox.checked = selectAll.checked;
      });
    },

    changeWeight() {
      this.items = [];
      this.loading = true;
      this.input = this.previous;
      if (this.toggle === true) {
        this.getRecommendResults2();
      } else {
        this.getRecommendResults();
      }
    },
    getSummaryInput() {
      this.showextractdisease = true;
      this.getExtractDiseaseResults();
    },
    updateDiseaseSet(active, item) {
      if (active === true) {
        for (let i = 0; i < this.target.length; i++) {
          if (this.target[i] === item) {
            this.target.splice(i, 1);
          }
        }
      } else {
        this.target.push(item);
      }
    },
    readyforRecommend() {
      this.showextractdisease = false;
      this.detail_search = false;
      this.summary = "";
      this.title = "";
      if (this.target.length === 0) this.target = this.extractdisease;
      this.target = this.target.map((element) => {
        return element.split("(")[0];
      });
      console.log(this.target);
      this.input = this.target.join(", ");
      this.target = [];
      this.extractdisease = [];
      this.re2();
    },

    chageapi() {
      this.toggle = !this.toggle;
      this.loading = true;

      if (this.toggle === true) {
        this.color = "cyan accent-6";
        this.click = "신규 ";
        this.input = this.previous;
        console.log(this.previous_items2);
        if (this.previous_items2 == null) {
          this.getRecommendResults2();
        } else {
          this.items = this.previous_items2;
          this.loading = false;
        }
      } else {
        this.color = "primary";
        this.click = "기존  ";
        this.input = this.previous;
        console.log(this.previous_items);
        if (this.previous_items == null) {
          this.getRecommendResults();
        } else {
          this.items = this.previous_items;
          this.loading = false;
        }
      }
      this.getCountResults();
      this.getDiseaseMatchResults();
      this.input = "";
    },

    re2() {
      this.loading = true;
      this.items = [];
      this.getRecommendResults();
      this.previous_items = this.items;
      this.getCountResults();
      this.getDiseaseMatchResults();
      this.toggle = false;
      this.color = "primary";
      this.click = "기존 ";
      this.previous = this.input;
      this.input = "";
    },
    async getRecommendResults() {
      try {
        const temp = this.input;
        const params = {
          input: temp,
          weight_paper: 10 - this.clinical.val,
          weight_trial: this.clinical.val,
        };
        const res = await api.recommend(params);
        this.items = res["data"];
        this.items = JSON.parse(this.items);
        console.log(this.items);
        this.previous_items = this.items;
        this.loading = false;
        for (var i = 0; i < this.items.length; i++) {
          const tmp_push = [this.items[i]["belong"], this.items[i]["name_kor"]];
          this.tmp_info.push(tmp_push);
        }
        console.log(this.tmp_info);
        console.log(JSON.stringify(this.tmp_info));
        localStorage.setItem("itemArray", JSON.stringify(this.tmp_info));
      } catch (err) {
        console.log(err);
      }
    },
    async getRecommendResults2() {
      try {
        const temp = this.input;
        const params = {
          input: temp,
          weight_paper: 10 - this.clinical.val,
          weight_trial: this.clinical.val,
        };
        const res = await api.recommend2(params);
        this.items = res["data"];
        console.log(this.items);
        this.items = JSON.parse(this.items);
        console.log(this.items);
        this.previous_items2 = this.items;
        this.loading = false;
      } catch (err) {
        console.log(err);
      }
    },
    async getCountResults() {
      try {
        const temp = this.input;

        const params = {
          input: temp,
        };

        const res = await api.getCount(params);

        let result = res["data"];
        result = JSON.parse(result);
        this.overall_count = result["overall_count"];
        this.partition_count = result["partition_count"];
      } catch (err) {
        console.log(err);
      }
    },
    async getDiseaseMatchResults() {
      try {
        const temp = this.input;
        const params = {
          input: temp,
        };
        const res = await api.getDiseaseMatch(params);
        let result = res["data"];
        this.diseasematch = JSON.parse(result);
      } catch (err) {
        console.log(err);
      }
    },
    async getExtractDiseaseResults() {
      try {
        const temp = this.summary;
        const params = {
          input: temp,
        };
        console.log(10 - this.clinical.val);
        console.log(this.clinical.val);
        const res = await api.getExtractDisease(params);
        let result = res["data"];
        this.extractdisease = JSON.parse(result);
      } catch (err) {
        console.log(err);
      }
    },
    async showParticipateInfo(item) {
      this.clinicalTrialsSearch = "";
      this.loadingDialog = true;
      try {
        const res = await api.getClinicalTrials(item.pid);
        const clinicalTrialsData = res.data;
        const clinicalTrialsItems = [];
        for (let data of clinicalTrialsData) {
          clinicalTrialsItems.push(data.clinical_trials);
        }
        clinicalTrialsItems.sort(function (a, b) {
          if (a.start_date === "") {
            return 1;
          } else if (b.start_date === "") {
            return -1;
          }
          return new Date(b.start_date) - new Date(a.start_date);
        });
        this.clinicalTrialsData = clinicalTrialsItems;
        this.loadingDialog = false;
        this.participateDialog = true;
      } catch (err) {
        console.log(err);
      }
    },
  },

  /*
  computed:{
    checkAll : { 
				//getter
				get: function(){
					if((this.select.length != this.history.length) || this.history.length == 0)
						return false;
					else
            console.log(this.select)
						return true;							
				},
				//setter
				set: function(e){
					
					if(e){
            this.select = true
						for(var i=0; i<this.history.length; i++){
              
							this.selected.push(this.history[i].selected);
						}	
					}
					else{
						this.select = false
						//this.selected = [];
					}
								
				}
			},

    selected:{
				get: function(){
					if((this.select.length != this.history.length) || this.history.length == 0)
						return false;
					else
            console.log("true")
						return true;							
				},
				//setter
				set: function(e){
					
					if(e){
            this.select = true

						for(var i=0; i<this.history.length; i++){
              
							this.selected.push(this.history[i].selected);
						}	

          }
					else{
						this.select = false
						//this.selected = [];
					}
								
				}

  
      }

    },
    */

  mounted: function () {
    this.input = this.$route.params.disease;
    if (this.input === "") this.input = "I20.1";
    this.previous = this.input;
    this.re2();
  },
};

</script>



<style>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap");

section {
  font-family: "Nanum Gothic", sans-serif;
}
p {
  font-family: "Nanum Gothic", sans-serif;
}

img {
  width: 4rem;
  height: 4rem;
  object-fit: cover;
  border-radius: 70%;
  padding: 0.5rem;
}

#network {
  left: 70px;
}

#all_check {
  position: relative;
  left: 5px;
  top: 4px;
}

</style>


<style scoped>
a:link {
  text-decoration: none;
}
a:visited {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>
