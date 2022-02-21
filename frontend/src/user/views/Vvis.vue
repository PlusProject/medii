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
        style="width: 50px"
      ></v-slider>
      <v-btn elevation="2" class="ml-5" @click="makeallnetwork">make</v-btn>
      <v-btn elevation="2" class="ml-5" @click="move">move</v-btn>
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
    items: [],
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
    value: null,
    nodes: [],
    edges: [],
    dialog: false,
    text: "논문",
    toget: 50,
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
    // options: {
    //   nodes: {
    //     borderWidth: 2,
    //     shape: "dot",
    //     font: { strokeWidth: 3, strokeColor: "white" },
    //   },
    //   edges: {
    //     color: "#024B28",
    //   },
    //   physics: {
    //     enabled: true,
    //     barnesHut: {
    //       theta: 0.5,
    //       gravitationalConstant: -10000,
    //       centralGravity: 0.3,
    //       springLength: 95,
    //       springConstant: 0.04,
    //       damping: 0.09,
    //       avoidOverlap: 0,
    //     },
    //     maxVelocity: 50,
    //     minVelocity: 0.1,
    //     solver: "barnesHut",
    //     stabilization: {
    //       enabled: true,
    //       iterations: 1000,
    //       updateInterval: 100,
    //       onlyDynamicEdges: false,
    //       fit: true,
    //     },
    //     timestep: 0.5,
    //     adaptiveTimestep: true,
    //     wind: { x: 0, y: 0 },
    //   },
    //   interaction: {
    //     hover: true,
    //   },
    // },
  }),
  mounted() {
    this.init();
  },
  methods: {
    async init() {
      try {
        this.makeallnetwork();
        this.$refs.network.moveTo({ scale: 0.3 });
        console.log("hi");
      } catch (err) {
        console.log(err);
      }
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

      const snpaperedgeyear = this.$store.state.snpaperedgeyear;
      const snpaper = this.$store.state.nodes;
      var maxd = 0;
      var together = [];
      for (let an of snpaperedgeyear) {
        var width = 0;
        for (let y of this.range(this.yearrange[0], this.yearrange[1]))
          width += an[String(y)];
        an["width"] = width;
        if (an["width"] >= this.toget && this.text != "center") {
          if (!together.includes(an["from"])) {
            together.push(an["from"]);
          }
          if (!together.includes(an["to"])) {
            together.push(an["to"]);
          }
          if (an["width"] > maxd) {
            maxd = an["width"];
          }
        }
      }
      var temp = {};
      for (let an of snpaper) {
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
          this.nodes.push(temp);
        } else if (an["clinical"] != 0 && this.text != "right") {
          temp = {};
          temp["id"] = an["id"];
          temp["color"] = an["color"];
          temp["value"] = an["value"];
          temp["label"] = an["label"];
          temp["title"] = an["title"];
          temp["shape"] = "dot";
          temp["belong"] = an["belong"];
          temp["borderWidth"] = an["borderWidth"];
          this.nodes.push(temp);
        }
      }
      for (let an of snpaperedgeyear) {
        if (an["width"] < this.toget || this.text == "center") continue;
        var edge = {};
        edge["from"] = an["from"];
        edge["to"] = an["to"];
        edge["color"] = "#024B28";
        edge["label"] = an["label"] + "(" + an["width"] + ")";
        edge["width"] =
          ((an["width"] - this.toget + 1) / (maxd - this.toget)) * 10;
        if (edge["width"] != 0) {
          edge["title"] =
            "공동 작업 논문 수: " +
            String(an["width"]) +
            "\n대표 질병 코드: " +
            an["label"];
          this.edges.push(edge);
        }
      }
      this.edges.sort(function (a, b) {
        return a["width"] - b["width"];
      });
      const crisedge = this.$store.state.crisedge;
      for (let an of crisedge) {
        var ce = {};
        ce["from"] = an["from"];
        ce["to"] = an["to"];
        ce["color"] = an["color"];
        ce["label"] = an["label"];
        ce["width"] = (an["width"] / 11) * 10;
        ce["title"] = an["title"];
        if (this.text != "right") this.edges.push(ce);
      }
    },
  },
};
</script>
