<template>
  <body>
    <v-toolbar flat class="pt-10 pe-10" color="#F3F5FF">
      <v-btn-toggle v-model="text" mandatory group color="deep-purple accent-3">
        <v-btn value="left"> 전체 </v-btn>

        <v-btn value="center"> 임상시험 </v-btn>

        <v-btn value="right"> 논문 </v-btn>
      </v-btn-toggle>

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
        max="50"
        min="1"
      ></v-slider>
      <v-btn elevation="2" class="ml-5" @click="makenetwork">make</v-btn>
      <v-menu bottom :offset-y="true" :close-on-click="false">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="primary" dark v-bind="attrs" v-on="on" class="ml-5">
            소속병원
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="(item, index) in belongs" :key="index">
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
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
    belongs: [
      { title: "노랑: 연세대 세브란스" },
      { title: "초록: 아산" },
      { title: "하늘: 삼성" },
      { title: "분홍: 가톨릭" },
      { title: "빨강: 고려대" },
      { title: "주황: 계명대" },
      { title: "보라: 서울대" },
      { title: "회색: 나머지" },
    ],
    closeOnClick: true,
    items: [],
    toget: 50,
    togets: { label: "연관성", color: "purple" },
    yearrange: [2005, 2022],
    years: { color: "green", fyear: 2005, label: "년도", lyear: 2022 },
    values: [],
    ids: [],
    nodes: [],
    edges: [],
    allnodes: [],
    alledges: [],
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
    this.getValues();
    this.makenetwork();
  },
  methods: {
    range(start, end) {
      let array = [];
      for (let i = start; i < end; ++i) {
        array.push(i);
      }
      return array;
    },
    getValues() {
      var select = this.$route.params.select;
      for (let sl of select) {
        this.values.push(sl["name_kor"] + "|" + sl["belong"]);
      }
    },
    makenetwork() {
      this.nodes = [];
      this.edges = [];
      const snpaperedgeyear = this.$store.state.snpaperedgeyear;
      const nodes = this.$store.state.nodes;
      const crisedge = this.$store.state.crisedge;
      this.ids = [];
      for (let value of this.values) {
        for (let an of nodes) {
          if (value.includes(an["label"]) && value.includes(an["belong"]))
            this.ids.push(an["id"]);
        }
      }
      var maxd = 0;
      var together = [];
      for (let an of snpaperedgeyear) {
        var width = 0;
        for (let y of this.range(this.yearrange[0], this.yearrange[1]))
          width += an[String(y)];
        an["width"] = width;
        if (an["width"] < this.toget) continue;
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
      var maxe = 0;
      var mine = 12;
      for (let an of crisedge) {
        if (this.ids.includes(an["to"]) && this.ids.includes(an["from"])) {
          if (an["cnt"] > maxe) {
            maxe = an["cnt"];
          }
          if (an["cnt"] < mine) {
            mine = an["cnt"];
          }
          continue;
        }
        if (this.ids.includes(an["to"]) && !together.includes(an["from"])) {
          together.push(an["from"]);
          if (an["cnt"] > maxe) {
            maxe = an["cnt"];
          }
          if (an["cnt"] < mine) {
            mine = an["cnt"];
          }
        }
        if (this.ids.includes(an["from"]) && !together.includes(an["to"])) {
          together.push(an["to"]);
          if (an["cnt"] > maxe) {
            maxe = an["cnt"];
          }
          if (an["cnt"] < mine) {
            mine = an["cnt"];
          }
        }
      }
      for (let id of this.ids) {
        together.push(id);
      }
      var temp = {};
      for (let an of nodes) {
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
          for (let vl of this.values) {
            if (vl.includes(an["label"]) && vl.includes(an["belong"]))
              temp["borderWidth"] = 10;
          }
          this.nodes.push(temp);
        }
      }
      for (let an of snpaperedgeyear) {
        width = 0;
        for (let y of this.range(this.yearrange[0], this.yearrange[1]))
          width += an[String(y)];
        an["width"] = width;
        if (an["width"] < this.toget) continue;
        if (!together.includes(an["from"]) || !together.includes(an["to"]))
          continue;
        var edge = {};
        edge["from"] = an["from"];
        edge["to"] = an["to"];
        edge["color"] = "#024B28";
        edge["label"] = an["label"] + "(" + an["width"] + ")";
        edge["width"] =
          ((an["width"] - this.toget + 1) / (maxd - this.toget)) * 10;
        edge["title"] =
          "공동 작성 논문 수: " + String(an["width"]) + "\n대표 질병 코드:";
        this.edges.push(edge);
      }
      this.edges.sort(function (a, b) {
        return a["width"] - b["width"];
      });
      for (let an of crisedge) {
        if (!together.includes(an["from"]) || !together.includes(an["to"]))
          continue;
        var ce = {};
        ce["from"] = an["from"];
        ce["to"] = an["to"];
        ce["color"] = an["color"];
        ce["label"] = an["label"];
        ce["width"] = ((an["cnt"] - mine + 1) / (maxe - mine)) * 10;
        ce["title"] = an["title"];
        this.edges.push(ce);
      } //*/
    },
  },
};
</script>
