<template>
  <body>
    <v-card>
      <v-container fluid>
        <v-row align="center">
          <v-col cols="12">
            <v-autocomplete
              v-model="value"
              :items="items"
              dense
              filled
              label="Filled"
            ></v-autocomplete>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-btn elevation="2" @click="makenetwork">make</v-btn>
    <div style="height: 800px; width: 100%; border: 1px solid gold">
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
    value: null,
    nodes: [],
    edges: [],
    allnodes: [],
    alledges: [],
    options: {
      nodes: {
        borderWidth: 2,
      },
      edges: {
        color: "#024B28",
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
  },
  methods: {
    async init() {
      try {
        for (var ed of this.$store.state.snpaper) {
          this.items.push(ed["label"] + "|" + ed["belong"]);
          this.allnodes.push(ed);
        }
        for (var an of this.$store.state.snpaperedgeyear)
          this.alledges.push(an);
      } catch (err) {
        console.log(err);
      }
    },
    makenetwork() {
      if (this.value != null) {
        this.nodes = [];
        this.edges = [];
        for (var an of this.allnodes) {
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
        for (an of this.$store.state.snpaperedgeyear) {
          if (an["2020"] + an["2021"] != 0) {
            if (an["from"] == this.ma) {
              toget.push(an["to"]);
              if (an["2020"] + an["2021"] > maxd) {
                maxd = an["2020"] + an["2021"];
                maxdd = [];
                maxdd.push(an["to"]);
              } else if (an["2020"] + an["2021"] == maxd) {
                maxdd.push(an["to"]);
              }
            } else if (an["to"] == this.ma) {
              toget.push(an["from"]);
              if (an["2020"] + an["2021"] > maxd) {
                maxd = an["2020"] + an["2021"];
                maxdd = [];
                maxdd.push(an["from"]);
              } else if (an["2020"] + an["2021"] == maxd) {
                maxdd.push(an["from"]);
              }
            }
          }
        }
        toget.push(this.ma);
        for (an of this.$store.state.snpaperedgeyear) {
          if (
            an["2020"] + an["2021"] != 0 &&
            toget.includes(an["from"]) &&
            toget.includes(an["to"])
          ) {
            if (an["2020"] + an["2021"] > maxed)
              maxed = an["2020"] + an["2021"];
          }
        }
        for (an of this.$store.state.snpaperedgeyear) {
          var edge = {};
          edge["from"] = an["from"];
          edge["to"] = an["to"];
          edge["width"] = ((an["2020"] + an["2021"]) / maxed) * 10;
          if (
            edge["width"] != 0 &&
            toget.includes(edge["from"]) &&
            toget.includes(edge["to"])
          ) {
            if (edge["from"] == this.ma || edge["to"] == this.ma)
              edge["color"] = "#FF6C7E";
            edge["title"] =
              "공동 작성 논문 수: " +
              String(an["2020"] + an["2021"]) +
              "\n대표 질병 코드:";

            this.edges.push(edge);
          }
        }
        toget = [];
        for (an of this.edges) {
          if (toget.includes(an["from"]) == false) toget.push(an["from"]);
          if (toget.includes(an["to"]) == false) toget.push(an["to"]);
        }
        var temp = null;
        for (an of this.$store.state.snpaper) {
          if (toget.includes(an["id"])) {
            temp = an;
            if (maxdd.includes(temp["id"])) temp["borderWidth"] = 10;
            this.nodes.push(an);
          }
        }
      }
    },
  },
};
</script>
