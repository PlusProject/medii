import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import api from "./api";
//import vis from "vis-network";

Vue.use(Vuex);
const state = {
  search: {
    name_kor: "",
    belong: "",
    major: "",
    disease: "",
  },
  doctorList: [],
  hospitalList: [],
  diseaseList: [],
  rareDiseaseList: [],
  person: [],
  doctor_info: [],
  participate: [],
  writes: [],
  snpaper50: [],
  snpapercnt50: [],
  snpaper: [],
  snpapercnt: [],
  nodecris: [],
  nodecriscnt: [],
  partpapernode: [],
  partpaperedge: [],
  snpaperedgeyear: [],
  //allnetwork: null,
  options: {
    nodes: {},
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
        gravitationalConstant: -80000,
        springLength: 200,
        springConstant: 0.001,
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
  showRareDisease: false,
  showClinicalTrialsPage: false,
};

const getters = {
  getQuery(state) {
    return state.search;
  },
  doctorList(state) {
    return state.doctorList.sort();
  },
  hospitalList(state) {
    return state.hospitalList.sort();
  },
  diseaseList(state) {
    return state.diseaseList.sort();
  },
  rareDiseaseList(state) {
    return state.rareDiseaseList.sort();
  },
  getPerson(state) {
    return state.person;
  },
  getParticipate(state) {
    return state.participate;
  },
  getWrites(state) {
    return state.writes;
  },
  getDoctorInfo(state) {
    return state.doctor_info;
  },
  getPersonLength(state) {
    return state.person.length;
  },
  getDoctorInfoLength(state) {
    return state.doctor_info.length;
  },
  showRareDisease(state) {
    return state.showRareDisease;
  },
  showClinicalTrialsPage(state) {
    return state.showClinicalTrialsPage;
  },
};

const mutations = {
  setDetailQuery(state, data) {
    (state.search.name_kor = data.name_kor || ""),
      (state.search.belong = data.belong || ""),
      (state.search.major = data.major || ""),
      (state.search.disease = data.disease || "");
  },
  setDiseaseQuery(state, data) {
    state.search.disease = data;
  },
  initAutocomplete(state, data) {
    state.doctorList = data.doctorList;
    state.hospitalList = data.hospitalList;
    state.diseaseList = data.diseaseList;
    state.rareDiseaseList = data.rareDiseaseList;
    state.snpaper50 = data.snpaper50;
    state.snpapercnt50 = data.snpapercnt50;
    state.snpaper = data.snpaper;
    state.snpapercnt = data.snpapercnt;
    state.nodecris = data.nodecris;
    state.nodecriscnt = data.nodecriscnt;
    state.partpapernode = data.partpapernode;
    state.partpaperedge = data.partpaperedge;
    state.snpaperedgeyear = data.snpaperedgeyear;
    //state.allnetwork = data.network;
  },
  savePersonInfo(state, data) {
    state.person = data;
  },
  clearState(state) {
    (state.person = []),
      (state.doctor_info = []),
      (state.participate = []),
      (state.writes = []);
  },
  clearSearchQuery(state) {
    const data = {
      name_kor: "",
      belong: "",
      major: "",
      disease: "",
    };
    state.search = data;
  },
  setShowRareDisease(state, data) {
    state.showRareDisease = data;
  },
  setShowClinicalTrialsPage(state, data) {
    state.showClinicalTrialsPage = data;
  },
};

const actions = {
  async initAutocomplete({ commit }) {
    const doctor = await api.getDoctorList();
    const hospital = await api.getHospitalList();
    const disease = await api.getDiseaseList();
    const rareDisease = await api.getRareDiseaseList();
    const doctorList = [];
    const hospitalList = [];
    const diseaseList = [];
    const rareDiseaseList = [];
    for (let name of doctor.data) {
      doctorList.push(name.name_kor);
    }
    for (let name of hospital.data) {
      hospitalList.push(name.belong);
    }
    for (let name of disease.data) {
      diseaseList.push(name.name_kor);
    }
    for (let name of rareDisease.data) {
      rareDiseaseList.push(name.name_kor);
    }

    const paper50 = await api.getSnPaper50();
    const snpaper50 = [];
    const papercnt50 = await api.getSnPaperCnt50();
    const snpapercnt50 = [];
    const paper = await api.getSnPaper();
    const snpaper = [];
    const papercnt = await api.getSnPaperCnt();
    const snpapercnt = [];
    const cris = await api.getNodeCris();
    const nodecris = [];
    const criscnt = await api.getNodeCrisCnt();
    const nodecriscnt = [];
    for (let name of paper50.data) {
      snpaper50.push(name);
    }
    for (let name of papercnt50.data) {
      var edge50 = {};
      edge50["from"] = name["fromit"];
      edge50["to"] = name["toit"];
      edge50["width"] = name["width"];
      snpapercnt50.push(edge50);
    }
    for (let name of cris.data) {
      nodecris.push(name);
    }
    for (let name of criscnt.data) {
      var crisedge = {};
      crisedge["from"] = name["fromit"];
      crisedge["to"] = name["toit"];
      crisedge["width"] = name["width"];
      crisedge["title"] = name["title"];
      nodecriscnt.push(crisedge);
    }
    for (let name of paper.data) {
      snpaper.push(name);
    }
    for (let name of papercnt.data) {
      var edge = {};
      edge["from"] = name["fromit"];
      edge["to"] = name["toit"];
      edge["width"] = name["width"];
      snpapercnt.push(edge);
    }

    const papernode = await api.getPartPaperNode();
    const partpapernode = [];
    const paperedge = await api.getPartPaperEdge();
    const partpaperedge = [];
    for (let name of papernode.data) {
      partpapernode.push(name);
    }
    for (let name of paperedge.data) {
      var pnedge = {};
      pnedge["from"] = name["fromit"];
      pnedge["to"] = name["toit"];
      pnedge["width"] = name["width"];
      partpaperedge.push(pnedge);
    }
    const snedgeyear = await api.getSnPaperEdgeYear();
    const snpaperedgeyear = [];
    for (let name of snedgeyear.data) {
      var edgeyear = {};
      edgeyear["from"] = name["fromit"];
      edgeyear["to"] = name["toit"];
      edgeyear["width"] = name["total"];
      edgeyear["2021"] = name["y2021"];
      edgeyear["2020"] = name["y2020"];
      edgeyear["2019"] = name["y2019"];
      edgeyear["2018"] = name["y2018"];
      edgeyear["2017"] = name["y2017"];
      edgeyear["2016"] = name["y2016"];
      edgeyear["2015"] = name["y2015"];
      edgeyear["2014"] = name["y2014"];
      edgeyear["2013"] = name["y2013"];
      edgeyear["2012"] = name["y2012"];
      edgeyear["2011"] = name["y2011"];
      edgeyear["2010"] = name["y2010"];
      edgeyear["2009"] = name["y2009"];
      edgeyear["2008"] = name["y2008"];
      edgeyear["2007"] = name["y2007"];
      edgeyear["2006"] = name["y2006"];
      edgeyear["2005"] = name["to2005"];
      snpaperedgeyear.push(edgeyear);
    }
    /*
    var nodes = new vis.DataSet(snpaper);

    // create an array with edges
    var edges = new vis.DataSet(snpaperedgeyear);

    // create a network
    var container = document.getElementById("mynetwork");

    // provide the data in the vis format
    var data1 = {
      nodes: nodes,
      edges: edges,
    };
    var options = {};

    // initialize your network!
    var network = new vis.Network(container, data1, options);*/

    const data = {
      doctorList,
      hospitalList,
      diseaseList,
      rareDiseaseList,
      snpaper50,
      snpapercnt50,
      snpaper,
      snpapercnt,
      nodecris,
      nodecriscnt,
      partpapernode,
      partpaperedge,
      snpaperedgeyear,
      //network,
    };
    commit("initAutocomplete", data);
  },
  commitSearchResults({ commit }, { data }) {
    commit("savePersonInfo", data);
  },
  clearState({ commit }) {
    commit("clearState");
  },
};

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: state,
  getters: getters,
  mutations: mutations,
  actions: actions,
});
