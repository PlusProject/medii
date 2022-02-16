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
  doctors: [
    "권현철|삼성서울병원",
    "박승정|서울아산병원",
    "나승운|고려대학교구로병원",
    "유상용|강릉아산병원",
  ],
  snpaperedgeyear: [],
  nodes: [],
  crisedge: [],
  scholaryear: [],
  alldisease: [],
  //allnetwork: null,
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
    state.snpaperedgeyear = data.snpaperedgeyear;
    state.nodes = data.nodes;
    state.crisedge = data.crisedge;
    state.scholaryear = data.scholaryear;
    state.alldisease = data.alldisease;
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

    const snedgeyear = await api.getSnPaperEdgeYear();
    const snpaperedgeyear = [];
    for (let name of snedgeyear.data) {
      var edgeyear = {};
      edgeyear["from"] = name["fromit"];
      edgeyear["to"] = name["toit"];
      edgeyear["label"] = name["disease"];
      edgeyear["total"] = name["total"];
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

    const nds = await api.getNodes();
    const nodes = [];
    for (let name of nds.data) {
      var ns = {};
      ns["id"] = name["id"];
      ns["label"] = name["label"];
      ns["belong"] = name["belong"];
      ns["color"] = name["color"];
      ns["value"] = ((name["paper_cnt"] + name["clinical_cnt"]) / 457) * 50;
      ns["title"] =
        "소속병원: " +
        name["belong"] +
        " | 대표 질병코드: " +
        name["disease"] +
        " | 논문 수: " +
        String(name["paper_cnt"]) +
        " | 임상시험 수: " +
        String(name["clinical_cnt"]);
      ns["shape"] = "dot";
      ns["borderWidth"] = 2;
      ns["clinical"] = name["clinical_cnt"];
      nodes.push(ns);
    }

    const ce = await api.getCrisEdge();
    const crisedge = [];
    for (let name of ce.data) {
      var c = {};
      c["from"] = name["fromit"];
      c["to"] = name["toit"];
      c["width"] = (name["cnt"] / 11) * 10;
      c["cnt"] = name["cnt"];
      c["label"] = name["title"] + "(" + name["cnt"] + ")";
      c["color"] = "#BC091F";
      c["title"] =
        "공동 작업 임상시험 수: " +
        String(name["cnt"]) +
        " | 질병코드: " +
        String(name["title"]);

      crisedge.push(c);
    }
    // initialize your network!

    const scyear = await api.getScholarYear();
    const scholaryear = [];
    for (let name of scyear.data) {
      edgeyear = {};
      edgeyear["from"] = name["fromit"];
      edgeyear["to"] = name["toit"];
      edgeyear["total"] = name["total"];
      edgeyear["match"] = 0;
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
      scholaryear.push(edgeyear);
    }
    const ad = await api.getAllDisease();
    const alldisease = [];
    for (let d of ad.data) {
      if (!alldisease.includes(d["disease_code"]))
        alldisease.push(d["disease_code"]);
    }

    const data = {
      doctorList,
      hospitalList,
      diseaseList,
      rareDiseaseList,
      crisedge,
      snpaperedgeyear,
      nodes,
      scholaryear,
      alldisease,
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
