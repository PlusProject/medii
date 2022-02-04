<template>
  <body>
    <v-row
      align="center"
      justify="space-around"
      class="pt-6"
      style="width: 50%"
    >
      <v-btn color="primary" @click="hidden = !hidden">
        {{ hidden ? "임상시험" : "논문" }}
      </v-btn>
      <v-btn color="primary" v-show="!hidden" @click="hidden50 = !hidden50">
        {{ hidden50 ? "1" : "50" }}
      </v-btn>
      <v-btn color="primary"> 소속병원 </v-btn>
    </v-row>
    <div id="app" style="height: auto; width: 100%; border: 1px solid gold">
      <network
        v-show="!hidden && hidden50"
        style="height: 800px"
        ref="network"
        :nodes="snpaper"
        :edges="this.$store.state.snpapercnt"
        :options="options"
        
      >
      </network>
      <network
        v-show="hidden"
        style="height: 800px"
        ref="network"
        :nodes="this.$store.state.nodecris"
        :edges="this.$store.state.nodecriscnt"
        :options="options"
      >
      </network>
      <network
        v-show="!hidden && !hidden50"
        style="height: 800px"
        ref="network"
        :nodes="this.$store.state.snpaper50"
        :edges="this.$store.state.snpapercnt50"
        :options="options"
      >
      </network>
    </div>
  </body>
</template>

<script>
//import { mapGetters } from "vuex";
import api from "../api";

export default {
  name: "SocialNetwork",
  data() {
    return {
      hidden: false,
      hidden50: false,
      snpaper: [],
      snpapercnt: [],
      edges: [],
      event: [{ afterDrawing: true, animationfinished: true }],
      options: {
        nodes: {
          borderWidth: 2,
        },
        edges: {
          color: "#024B28",
          /*
          arrows: {
            to: { enabled: true, scaleFactor: 1, type: "arrow" },
          },
          */
        },
        groups: {
          myGroup: { color: { background: "red" }, borderWidth: 3 },
        },
        physics: {
          // enabled: true,
          // barnesHut: {
          //   theta: 0.5,
          //   gravitationalConstant: -2000,
          //   centralGravity: 0.1,
          //   springLength: 95,
          //   springConstant: 0.04,
          //   damping: 0.09,
          //   avoidOverlap: 0,
          // },
          // forceAtlas2Based: {
          //   theta: 0.5,
          //   gravitationalConstant: -50,
          //   centralGravity: 0.01,
          //   springConstant: 0.08,
          //   springLength: 100,
          //   damping: 0.4,
          //   avoidOverlap: 0,
          // },
          // repulsion: {
          //   centralGravity: 0.1,
          //   springLength: 50,
          //   springConstant: 0.05,
          //   nodeDistance: 100,
          //   damping: 0.09,
          // },
          // hierarchicalRepulsion: {
          //   centralGravity: 0.5,
          //   springLength: 150,
          //   springConstant: 0.01,
          //   nodeDistance: 60,
          //   damping: 0.09,
          //   avoidOverlap: 0,
          // },
          // maxVelocity: 50,
          // minVelocity: 0.1,
          // solver: "barnesHut",
          // stabilization: {
          //   enabled: true,
          //   iterations: 1000,
          //   updateInterval: 100,
          //   onlyDynamicEdges: false,
          //   fit: true,
          // },
          // timestep: 1,
          // adaptiveTimestep: true,
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
    };
  },
  mounted() {
    this.init();
    this.getSnPaper();
    this.getSnPaperCnt();
  },
  computed: {},
  watch: {
    getQuery() {
      this.resultRender = JSON.parse(JSON.stringify(this.getQuery));
      this.init();
    },
  },
  methods: {
    async init() {
      this.tableData = [];
    },
    async getSnPaper() {
      try {
        const res = await api.getSnPaper();
        this.snpaper = res.data;
      } catch (err) {
        console.log(err);
      }
    },
    async getSnPaperCnt() {
      try {
        const res = await api.getSnPaperCnt();
        this.snpapercnt = res.data;
        for (var sn in this.snpapercnt) {
          var edge = {};
          edge["from"] = this.snpapercnt[sn]["fromit"];
          edge["to"] = this.snpapercnt[sn]["toit"];
          edge["width"] = this.snpapercnt[sn]["width"];
          this.edges.push(edge);
        }
      } catch (err) {
        console.log(err);
      }
    },
  },
};
</script>
<style>
#lateral .v-btn--example {
  bottom: 0;
  position: absolute;
  margin: 0 0 16px 16px;
}
</style>
