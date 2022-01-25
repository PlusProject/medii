<template>
  <body>
    <v-btn color="primary" @click="hidden = !hidden">
      {{ hidden ? "임상시험" : "논문" }}
    </v-btn>
    <v-btn color="primary" @click="hidden50 = !hidden50">
      {{ hidden50 ? "0" : "50" }}
    </v-btn>
    <div id="app" style="height: auto; width: 100%; border: 1px solid gold">
      <network
        v-show="!hidden && hidden50"
        style="height: 800px"
        ref="network"
        :nodes="snpaper"
        :edges="edges"
        :options="options"
      >
      </network>
      <network
        v-show="hidden"
        style="height: 800px"
        ref="network"
        :nodes="nodecris"
        :edges="newedges"
        :options="options"
      >
      </network>
      <network
        v-show="!hidden && !hidden50"
        style="height: 800px"
        ref="network"
        :nodes="snpaper50"
        :edges="edges50"
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
      snpaper50: [],
      snpapercnt50: [],
      edges50: [],
      nodecris: [],
      nodecriscnt: [],
      newedges: [],
      desserts: [
        {
          name: "Frozen Yogurt",
          color: "#4ED4FE",
        },
      ],
      test: [
        { id: 1, label: "2", group: "myGroup" },
        { id: 2, label: "3", group: "myGroup" },
        { id: 3, label: "3" },
      ],
      teste: [{ from: 1, to: 2, title: "hi" }],
      edges: [],
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
          enabled: true,
          barnesHut: {
            theta: 0.5,
            gravitationalConstant: -2000,
            centralGravity: 0.1,
            springLength: 95,
            springConstant: 0.04,
            damping: 0.09,
            avoidOverlap: 0,
          },
          forceAtlas2Based: {
            theta: 0.5,
            gravitationalConstant: -50,
            centralGravity: 0.01,
            springConstant: 0.08,
            springLength: 100,
            damping: 0.4,
            avoidOverlap: 0,
          },
          repulsion: {
            centralGravity: 0.1,
            springLength: 50,
            springConstant: 0.05,
            nodeDistance: 100,
            damping: 0.09,
          },
          hierarchicalRepulsion: {
            centralGravity: 0.5,
            springLength: 150,
            springConstant: 0.01,
            nodeDistance: 60,
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
          timestep: 1,
          adaptiveTimestep: true,
        },
      },
    };
  },
  mounted() {
    this.init();
    this.getSnPaper();
    this.getSnPaperCnt();
    this.getNodeCris();
    this.getNodeCrisCnt();
    this.getSnPaper50();
    this.getSnPaperCnt50();
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
    async getNodeCris() {
      try {
        const res = await api.getNodeCris();
        this.nodecris = res.data;
      } catch (err) {
        console.log(err);
      }
    },
    async getNodeCrisCnt() {
      try {
        const res = await api.getNodeCrisCnt();
        this.nodecriscnt = res.data;
        for (var sn in this.nodecriscnt) {
          var edge = {};
          edge["from"] = this.nodecriscnt[sn]["fromit"];
          edge["to"] = this.nodecriscnt[sn]["toit"];
          edge["width"] = this.nodecriscnt[sn]["width"];
          edge["title"] = this.nodecriscnt[sn]["title"];
          this.newedges.push(edge);
        }
      } catch (err) {
        console.log(err);
      }
    },
    async getSnPaper50() {
      try {
        const res = await api.getSnPaper50();
        this.snpaper50 = res.data;
      } catch (err) {
        console.log(err);
      }
    },
    async getSnPaperCnt50() {
      try {
        const res = await api.getSnPaperCnt50();
        this.snpapercnt50 = res.data;
        for (var sn in this.snpapercnt50) {
          var edge = {};
          edge["from"] = this.snpapercnt50[sn]["fromit"];
          edge["to"] = this.snpapercnt50[sn]["toit"];
          edge["width"] = this.snpapercnt50[sn]["width"];
          this.edges50.push(edge);
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
