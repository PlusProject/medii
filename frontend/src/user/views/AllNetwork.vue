<template>
  <body>
    <v-toolbar flat class="pt-10 pe-10" color="#F3F5FF">
      <v-container fluid style="width: 250px">
        <v-autocomplete
          v-model="doctors"
          :items="doctorlist"
          dense
          chips
          small-chips
          multiple
          filled
          label="의료진"
        ></v-autocomplete>
      </v-container>
      <v-container fluid style="width: 300px">
        <v-autocomplete
          v-model="diseases"
          :items="diseaselist"
          dense
          chips
          small-chips
          multiple
          filled
          label="질병코드"
        ></v-autocomplete>
      </v-container>
      <v-range-slider
        v-model="yearrange"
        :color="years.color"
        :label="years.label"
        thumb-label="always"
        max="2022"
        min="2005"
      ></v-range-slider>
      <v-slider
        v-model="toget"
        :color="togets.color"
        :label="togets.label"
        class="ml-10"
        thumb-label="always"
        max="20"
        min="1"
        style="width: 50px"
      ></v-slider>
      <v-btn elevation="2" class="ml-5" @click="makeallnetwork">make</v-btn>
      <v-btn elevation="2" class="ml-5" @click="move">move</v-btn>
<v-btn color="primary" v-on:click="toggleShow">
        소속병원
      </v-btn>
      <div id = "list" v-if="show">
        <a style="background-color:#FBFF38">연세대</a><br>
        <a style="background-color:#67F942">아산</a><br>
        <a style="background-color:#4ED4FE">삼성</a><br>
        <a style="background-color:#FFA7B1">가톨릭</a><br>
        <a style="background-color:#FF6C7E">고려대</a><br>
        <a style="background-color:#FFB169">계명대</a><br>
        <a style="background-color:#DDB1FF">서울대</a><br>
        <a style="background-color:#C4C4C4">나머지</a>
      </div>
      <v-btn fab color="cyan accent-2" @click="dialog = !dialog" class="ml-5">
        <v-icon> mdi-comment-question </v-icon>
      </v-btn>

      <v-dialog v-model="dialog" max-width="850px">
        <v-card class="text-sm-left pa-7">
          <v-card-title>버튼 설명</v-card-title>

          <p class="blue lighten-3">MAKE</p>
          <v-spacer></v-spacer>
          <p>원하는 설정으로 바꾼 뒤 클릭 시 해당 설정에 맞춰서 네트워킹</p>
          <p class="blue lighten-3">MOVE</p>
          <p>
            <v-spacer></v-spacer>
          </p>

          <p>
            보고 싶은 의료진의 노드 선택 후 클릭 시 해당 의료진의 개별 네트워크
            페이지로 가짐
          </p>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn text color="primary" @click="dialog = false"> Close </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-toolbar>
    <div
      style="height: 800px; width: 100%; border: 1px solid gold"
      class="mt-10"
    >
      <network
        style="height: 800px"
        ref="network"
        :nodes="nodes"
        :edges="edges"
        :options="options"
      >
      </network>
    </div>
  </body>
</template>
<script>
export default {
  data: () => ({
    show:true,
    belongs: [
      { title: "노랑: 연세대 세브란스" },
      { title: "초록: 아산" },
      { title: "하늘: 삼성" },
      { title: "빨강: 가톨릭" },
      { title: "분홍: 고려대" },
      { title: "주황: 계명대" },
      { title: "보라: 서울대" },
      { title: "회색: 나머지" },
    ],
    doctorlist: [],
    diseaselist: [],
    doctors: [],
    ids: [],
    diseases: [],
    dialog: false,
    value: null,
    values: [],
    nodes: [],
    edges: [],
    text: "논문",
    toget: 7,
    togets: { label: "연관성", color: "purple" },
    yearrange: [2005, 2022],
    years: { color: "green", fyear: 2005, label: "년도", lyear: 2022 },
    options: {
      nodes: {
        borderWidth: 2,
        font: { strokeWidth: 3, strokeColor: "white" },
      },
      edges: {
        font: { strokeWidth: 2, strokeColor: "white" },
      },
      physics: {
        enabled: true,
        barnesHut: {
          theta: 0.5,
          gravitationalConstant: -10000,
          centralGravity: 0.3,
          springLength: 95,
          springConstant: 0.04,
          damping: 0.09,
          avoidOverlap: 0,
        },
        maxVelocity: 50,
        minVelocity: 0.1,
        solver: "barnesHut",
        stabilization: {
          enabled: true,
          iterations: 1000,
          updateInterval: 100,
          onlyDynamicEdges: false,
          fit: true,
        },
        timestep: 0.5,
        adaptiveTimestep: true,
        wind: { x: 0, y: 0 },
      },
    },
  }),
  mounted() {
    this.init();
  },
  methods: {
    toggleShow(){
      this.show = !this.show; 
    },
    async init() {
      try {
        this.getParams();
        this.makedoctorlist();
        this.makediseaselist();
        this.makeallnetwork();
        this.$refs.network.moveTo({ scale: 1 });
        console.log("hi");
      } catch (err) {
        console.log(err);
      }
    },
    getParams() {
      var select = this.$route.params.select;
      this.doctors = [];
      for (let sl of select) {
        this.doctors.push(sl["name_kor"] + "|" + sl["belong"]);
      }
      var dis = this.$route.params.disease;
      var di = [];
      this.diseases = [];
      if (dis.includes(",")) {
        di = dis.split(",");
        for (var d of di) {
          if (d[0] == " ") d = d.substring(1);
          this.diseases.push(d);
        }
      } else this.diseases = [dis];
    },
    makedoctorlist() {
      for (var ed of this.$store.state.nodes) {
        this.doctorlist.push(ed["label"] + "|" + ed["belong"]);
      }
    },
    makediseaselist() {
      this.diseaselist = this.$store.state.alldisease;
    },
    move() {
      this.$router.push({
        name: "jstest",
        params: {
          id: this.$refs.network.getSelection().nodes[0],
          toget: this.toget,
          fyear: this.yearrange[0],
          lyear: this.yearrange[1],
        },
      });
    },
    range(start, end) {
      let array = [];
      for (let i = start; i < end; ++i) {
        array.push(i);
      }
      return array;
    },
    makeallnetwork() {
      this.nodes = [];
      this.edges = [];

      const scholaryear = this.$store.state.scholaryear;
      const node = this.$store.state.nodes;
      const crisedge = this.$store.state.crisedge;
      var maxd = 0;
      var together = [];
      var str = "";
      var array = [];
      var dis = [];
      var width = 0;
      var dict = {};
      var label = "";
      this.ids = [];
      for (let value of this.doctors) {
        for (let an of node) {
          if (value.includes(an["label"]) && value.includes(an["belong"]))
            this.ids.push(an["id"]);
        }
      }
      for (let an of scholaryear) {
        width = 0;
        label = "";
        dict = {};
        for (let y of this.range(this.yearrange[0], this.yearrange[1])) {
          if (an[String(y)] == "") continue;
          str = an[String(y)];
          array = str.split("|");
          for (let ar of array) {
            dis = ar.split(":");
            if (this.diseases.includes(dis[0])) {
              width += Number(dis[1]);
              if (dis[0] in dict) dict[dis[0]] += Number(dis[1]);
              else dict[dis[0]] = Number(dis[1]);
            }
          }
        }
        for (var key in dict) {
          label += key + "(" + String(dict[key]) + ")|";
        }
        an["label"] = label;
        an["width"] = width;
        if (an["width"] >= this.toget) {
          if (this.ids.includes(an["to"]) && this.ids.includes(an["from"])) {
            if (an["width"] > maxd) maxd = an["width"];
            continue;
          }
          if (this.ids.includes(an["from"]) && !together.includes(an["to"])) {
            together.push(an["to"]);
            if (an["width"] > maxd) maxd = an["width"];
          } else if (
            this.ids.includes(an["to"]) &&
            !together.includes(an["from"])
          ) {
            together.push(an["from"]);
            if (an["width"] > maxd) maxd = an["width"];
          }
        }
      }
      for (let an of crisedge) {
        if (this.ids.includes(an["to"]) && this.ids.includes(an["from"]))
          continue;
        if (this.ids.includes(an["from"]) && !together.includes(an["to"]))
          together.push(an["to"]);
        else if (this.ids.includes(an["to"]) && !together.includes(an["from"]))
          together.push(an["from"]);
      }
      for (let id of this.ids) together.push(id);

      var temp = {};
      for (let an of node) {
        if (together.includes(an["id"])) {
          temp = {};
          temp["id"] = an["id"];
          temp["color"] = an["color"];
          temp["value"] = an["value"];
          temp["label"] = an["label"];
          temp["title"] = an["title"];
          temp["shape"] = "dot";
          temp["belong"] = an["belong"];
          temp["borderWidth"] = an["borderWidth"];
          if (this.ids.includes(an["id"])) temp["borderWidth"] = 10;

          this.nodes.push(temp);
        } /*
        else if (an["clinical"] != 0) {
          temp = {};
          temp["id"] = an["id"];
          temp["color"] = an["color"];
          temp["value"] = an["value"];
          temp["label"] = an["label"];
          temp["title"] = an["title"];
          temp["shape"] = "dot";
          temp["belong"] = an["belong"];
          temp["borderWidth"] = an["borderWidth"];
          if (this.ids.includes(an["id"])) temp["borderWidth"] = 10;

          this.nodes.push(temp);
        }//*/
      }
      for (let an of scholaryear) {
        if (an["width"] < this.toget) continue;
        if (this.value != null && this.value != an["label"]) continue;
        var edge = {};
        edge["from"] = an["from"];
        edge["to"] = an["to"];
        edge["color"] = "#024B28";
        edge["label"] = an["label"].substring(0, an["label"].length - 1);
        edge["width"] =
          ((an["width"] - this.toget + 1) / (maxd - this.toget)) * 10;
        if (edge["width"] != 0) {
          edge["title"] =
            "공동 작업 논문 수: " +
            String(an["width"]) +
            "\n대표 질병 코드: " +
            an["label"].substring(1);
          this.edges.push(edge);
        }
      }
      this.edges.sort(function (a, b) {
        return a["width"] - b["width"];
      });

      for (let an of crisedge) {
        var ce = {};
        ce["from"] = an["from"];
        ce["to"] = an["to"];
        ce["color"] = an["color"];
        ce["label"] = an["label"];
        ce["width"] = (an["width"] / 11) * 10;
        ce["title"] = an["title"];
        this.edges.push(ce);
      }
    },
  },
};
</script>
<style scoped>
#list{
  background-color: rgba(219, 219, 219, 0.5); 
  width:100px;
  position:absolute;
  top:63px;
  right:90px;
  border-radius:0.5rem;
}
</style>
