<template>
  <div class="wrapper">
    <h2>추천된 사람들 간의 Social Network</h2>
    <!--
    <div id='app'> 
        <input type="checkbox" v-model="arr" value="논문">논문 
        <input type="checkbox" v-model="arr" value="임상시험">임상시험
        <button @click='checkArr()'>check</button> 
    </div>
-->
    <network
      class="network"
      ref="network"
      :nodes="network.nodes"
      :edges="network.edges"
      :options="network.options"
    ></network>
        <img
      id="scream"
      src="north_pole.png"
      style="display: none;"
      alt="Noth Pole"
    />
  </div>
</template>

<script>
  import { Network } from "vue-vis-network";


  let defNodes = [
    { id: 1, label: "최동주", shape:"circle",color:"#5ECB3D"},
    { id: 2, label: "이지현", shape:"circle",color:"#5ECB3D"},
    { id: 3, label: "윤창환", shape:"circle",color:"#5ECB3D"},

  ]

let defEdges = [
        { id: 1, from: 1, to: 2 ,width:5,length:200},
        { id: 2, from: 1, to: 3 ,width:5,length:200},
      ]

export default {
  data: () => ({
    networkEvents: "",
    network: {
      nodes: defNodes.slice(0),
      edges: defEdges.slice(0),
      options: {
        nodes: {
          shape: "circle",
          size:24,
          color: {
            border: 'grey',
            
            highlight: {
              border: 'black',
              background: 'white'
            },
            hover: {
              border: 'orange',
              background: 'grey'
            }
          },
          font:{color:'black'},
          shapeProperties: {
            useBorderWithImage:true
          }
        }
      }
    }
  }),
  components: {
    Network
  },
  methods: {

    drawBg(ctx) {
      let mapBgWidth = document.getElementById("scream").width;
      let mapBgHeight = document.getElementById("scream").height;

      ctx.drawImage(
        document.getElementById("scream"),
        -mapBgWidth / 2,
        -mapBgHeight / 2
      );
    },
    
  }
};

</script>

<style>
* {
  font-family: sans-serif;
}

.wrapper {
  padding: 20px 50px;
  text-align: center;
}
.events {
  text-align: left;
  height: 70px;
}

.network {
  height: 400px;
  border: 1px solid #ccc;
  margin: 5px 0;
}
</style>