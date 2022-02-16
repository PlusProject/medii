<template>
  <body>
    <v-toolbar flat class="pt-10 pe-10" color="#F3F5FF">
      <v-container fluid style="width: 300px">
        <v-autocomplete
          v-model="value"
          :items="items"
          dense
          filled
          label="Filled"
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
        max="50"
        min="1"
      ></v-slider>
      <v-btn elevation="2" @click="makenetwork" class="ml-5">make</v-btn>
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
      <v-menu bottom :offset-y="true" :close-on-click="false">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="teal" dark v-bind="attrs" v-on="on" class="ml-5">
            순위
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="(item, index) in ranks" :key="index">
            <v-list-item-title>{{
              index + 1 + ": " + item.name + ", " + item.count
            }}</v-list-item-title>
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
    closeOnClick: true,
    dialog: false,
    items: [],
    toget: 50,
    togets: { label: "연관성", color: "purple" },
    yearrange: [2005, 2022],
    years: { color: "green", fyear: 2005, label: "년도", lyear: 2022 },
    value: null,
    lastvalue: null,
    nodes: [],
    edges: [],
    ranks: [],
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
    ma: null,
  }),
  mounted() {
    this.init();
    if (this.$route.params.id != null) {
      this.yearrange = [this.$route.params.fyear, this.$route.params.lyear];
      this.toget = this.$route.params.toget;
      const snpaper = this.$store.state.nodes;
      for (let an of snpaper) {
        if (an["id"] == this.$route.params.id) {
          this.value = an["label"] + "|" + an["belong"];
          break;
        }
      }
      console.log(this.$route.params);
      this.makenetwork();
    }
  },
  methods: {
    async init() {
      try {
        for (var ed of this.$store.state.nodes) {
          this.items.push(ed["label"] + "|" + ed["belong"]);
          this.allnodes.push(ed);
        }
        for (var an of this.$store.state.snpaperedgeyear)
          this.alledges.push(an);
      } catch (err) {
        console.log(err);
      }
    },
    move() {
      const node = this.$store.state.nodes;
      for (let nd of node) {
        if (nd["id"] == this.$refs.network.getSelection().nodes[0])
          this.value = nd["label"] + "|" + nd["belong"];
      }
      this.makenetwork();
    },
    range(start, end) {
      let array = [];
      for (let i = start; i < end; ++i) {
        array.push(i);
      }
      return array;
    },
    makenetwork() {
      if (this.value != null) {
        this.lastvalue = this.value;
        this.nodes = [];
        this.edges = [];
        this.ranks = [];

        const snpaperedgeyear = this.$store.state.snpaperedgeyear;
        const snpaper1 = this.$store.state.nodes;
        //const cris = this.$store.state.nodecris;
        //const criscnt = this.$store.state.nodecriscnt;
        for (let an of snpaper1) {
          if (
            this.value.includes(an["label"]) &&
            this.value.includes(an["belong"])
          ) {
            this.ma = an["id"];
            break;
          }
        }
        var toget = [];
        var maxed = 0;
        var maxd = 0;
        var maxdd = [];
        var rank = {};
        for (let an of snpaperedgeyear) {
          var width = 0;
          for (let y of this.range(this.yearrange[0], this.yearrange[1]))
            width += an[String(y)];
          an["width"] = width;
          if (an["width"] >= this.toget) {
            if (an["from"] == this.ma) {
              rank = {};
              rank["id"] = an["to"];
              rank["count"] = an["width"];
              this.ranks.push(rank);
              toget.push(an["to"]);
              if (an["width"] > maxd) {
                maxd = an["width"];
                maxdd = [];
                maxdd.push(an["to"]);
              } else if (an["width"] == maxd) {
                maxdd.push(an["to"]);
              }
            } else if (an["to"] == this.ma) {
              toget.push(an["from"]);
              rank = {};
              rank["id"] = an["from"];
              rank["count"] = an["width"];
              this.ranks.push(rank);
              if (an["width"] > maxd) {
                maxd = an["width"];
                maxdd = [];
                maxdd.push(an["from"]);
              } else if (an["width"] == maxd) {
                maxdd.push(an["from"]);
              }
            }
          }
        }
        toget.push(this.ma);
        for (let an of snpaperedgeyear) {
          if (
            an["width"] != 0 &&
            toget.includes(an["from"]) &&
            toget.includes(an["to"])
          ) {
            if (an["width"] > maxed) maxed = an["width"];
          }
        }
        for (let an of snpaperedgeyear) {
          if (an["width"] < this.toget) continue;
          var edge = {};
          edge["from"] = an["from"];
          edge["to"] = an["to"];
          edge["color"] = "#024B28";
          edge["label"] = an["label"] + "(" + an["width"] + ")";
          edge["width"] =
            ((an["width"] - this.toget + 1) / (maxd - this.toget)) * 10;
          if (
            edge["width"] != 0 &&
            toget.includes(edge["from"]) &&
            toget.includes(edge["to"])
          ) {
            if (edge["from"] == this.ma || edge["to"] == this.ma)
              edge["color"] = "#0400BB";
            edge["title"] =
              "공동 작업 논문 수: " +
              String(an["width"]) +
              " | 대표 질병 코드: " +
              an["label"];

            this.edges.push(edge);
          }
        }
        const crisedge = this.$store.state.crisedge;
        for (let an of crisedge) {
          var ce = {};
          ce["from"] = an["from"];
          ce["to"] = an["to"];
          ce["color"] = an["color"];
          if (an["from"] == this.ma || an["to"] == this.ma)
            ce["color"] = "#A839FF";
          ce["label"] = an["label"];
          ce["width"] = (an["width"] / 11) * 10;
          ce["title"] = an["title"];
          if (toget.includes(an["from"]) && toget.includes(an["to"]))
            this.edges.push(ce);
        }
        toget = [];
        for (let an of this.edges) {
          if (toget.includes(an["from"]) == false) toget.push(an["from"]);
          if (toget.includes(an["to"]) == false) toget.push(an["to"]);
        }
        var temp = {};
        for (let an of snpaper1) {
          if (toget.includes(an["id"])) {
            temp = {};
            temp["id"] = an["id"];
            temp["color"] = an["color"];
            temp["value"] = an["value"];
            temp["label"] = an["label"];
            temp["title"] = an["title"];
            temp["shape"] = "dot";
            temp["belong"] = an["belong"];
            temp["borderWidth"] = an["borderWidth"];
            if (maxdd.includes(an["id"])) temp["borderWidth"] = 10;
            if (temp["id"] == this.ma) {
              var co = {};
              co["background"] = temp["color"];
              co["border"] = "#0400BB";
              temp["color"] = co;
              temp["borderWidth"] = 10;
            }
            this.nodes.push(temp);
          }
        }
        this.edges.sort(function (a, b) {
          return a["width"] - b["width"];
        });
        for (let rk of this.ranks) {
          for (let nd of this.nodes) {
            if (nd["id"] == rk["id"]) {
              rk["name"] = nd["label"] + "|" + nd["belong"];
              rk["size"] = nd["value"];
              break;
            }
          }
        }
        this.ranks.sort(function (a, b) {
          if (a["count"] == b["count"]) {
            return -a["size"] + b["size"];
          }
          return -a["count"] + b["count"];
        });
      }
    },
  },
};
</script>
