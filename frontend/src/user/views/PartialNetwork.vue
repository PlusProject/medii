<template>
  <div class = "myDiv">
      <div id="viz"></div>
    <div>
    <div id="choose">
    <input type="submit" value="전체 네트워킹 보기" id="total" @click="total"><br>
    <input type="submit" value="논문 네트워킹만 보기" id="paper" @click="paper"><br>
    <input type="submit" value="임상시험 네트워킹만 보기" id="test" @click="test">
    </div>

    <div id = "search">
        <div id="search_name">검색: <input type="text" id="cypher"></div><br>
        <input type="submit" value="전체 네트워킹 검색" id="part_total" @click="part_total"><br>
        <input type="submit" value="논문 네트워킹 검색" id="part_paper" @click="part_paper"><br>
        <input type="submit" value="임상시험 네트워킹 검색" id="part_test" @click="part_test">
    </div>
    <div id = "stop">
    <input type="submit" value="멈춤" id="stabilize" @click="stabilize">
    </div>
    </div>
  </div>
</template>

<script>
export default {
    name: '',
    data(){
        return{
            viz: {},
            get_array:[],
            name_list:''
        }
    },
    mounted(){
        this.get_storage(),
        this.get_namelist(),
        this.draw()
    },
    methods:{
        get_storage(){
            //console.log(localStorage.getItem('itemArray'))
            this.get_array = JSON.parse(localStorage.getItem('itemArray'))
            //console.log(output)
            //this.get_array = output
            console.log(this.get_array)
        },
        total(){           
            var nameSplit = this.name_list.split(',');
            var str = ""
            console.log(nameSplit.length)
            for(var i = 0; i<nameSplit.length-1; i++){
                str +=  'n.name="'+nameSplit[i]+ '" or '
                //console.log(str)
            }
            str += 'n.name="' + nameSplit[nameSplit.length-1] + '"'
            console.log(str)
            var cypher = 'MATCH (n)-[r]->(m) where '+str+' RETURN n,r,m'
            
            console.log(cypher)
            this.get_total_val;
            console.log(this.total_val)
            if (cypher.length > 3) {
                this.viz.renderWithCypher(cypher);
            } else {
                console.log("reload");
                this.viz.reload();
    
            }
        },
        paper(){          
            var nameSplit = this.name_list.split(',');
            var str = ""
            console.log(nameSplit.length)
            for(var i = 0; i<nameSplit.length-1; i++){
                str +=  'n.name="'+nameSplit[i]+ '" or '
                console.log(str)
            }
            str += 'n.name="' + nameSplit[nameSplit.length-1] + '"'
            console.log(str)
            var cypher = 'MATCH (n)-[r:`논문`]->(m) where '+str+' RETURN n,r,m'
            console.log(cypher)
            if (cypher.length > 3) {
                this.viz.renderWithCypher(cypher);
            } else {
                console.log("reload");
                this.viz.reload();
    
            }
        },
        test(){          
            var nameSplit = this.name_list.split(',');
            var str = ""
            console.log(nameSplit.length)
            for(var i = 0; i<nameSplit.length-1; i++){
                str +=  'n.name="'+nameSplit[i]+ '" or '
                console.log(str)
            }
            str += 'n.name="' + nameSplit[nameSplit.length-1] + '"'
            console.log(str)
            var cypher = 'MATCH (n)-[r:`임상시험`]->(m) where '+str+' RETURN n,r,m'
            console.log(cypher)
            if (cypher.length > 3) {
                this.viz.renderWithCypher(cypher);
            } else {
                console.log("reload");
                this.viz.reload();
            }
        },
        get_namelist(){
            for(var i = 0 ; i<this.get_array.length-1;i++){
                if(this.get_array[i][1] == "박승정"){
                    if(this.get_array[i][0] == "서울아산병원"){
                        this.name_list += "박승정_아산"
                    }
                    else{
                        this.name_list += "박승정_삼성"
                    }
                }
                else if(this.get_array[i][1] == "김지훈"){
                    if(this.get_array[i][0] == "서울삼성병원"){
                        this.name_list += "김지훈_삼성"
                    }
                    else{
                        this.name_list += "김지훈_가톨릭"
                    }
                }
                else if(this.get_array[i][1] == "김태훈"){
                    if(this.get_array[i][0] == "연세대학교세브란스병원"){
                        this.name_list += "김태훈_세브란스"
                    }
                    else{
                        this.name_list += "김태훈_강남세브란스"
                    }
                }
                else if(this.get_array[i][1] == "서지원"){
                    if(this.get_array[i][0] == "연세대학교세브란스병원"){
                        this.name_list += "서지원_세브란스"
                    }
                    else{
                        this.name_list += "서지원_용인세브란스"
                    }
                }             
                else {
                    this.name_list+=this.get_array[i][1]
                }
                this.name_list+=','
            }
            if(this.get_array[this.get_array.length-1][1] == "박승정"){
                if(this.get_array[this.get_array.length-1][0] == "서울아산병원"){
                    this.name_list += "박승정_아산"
                }
                else{
                    this.name_list += "박승정_삼성"
                }
            }
            else if(this.get_array[this.get_array.length-1][1] == "김지훈"){
                if(this.get_array[this.get_array.length-1][0] == "서울삼성병원"){
                    this.name_list += "김지훈_삼성"
                }
                else{
                    this.name_list += "김지훈_가톨릭"
                }
            }
            else if(this.get_array[this.get_array.length-1][1] == "김태훈"){
                if(this.get_array[this.get_array.length-1][0] == "연세대학교세브란스병원"){
                    this.name_list += "김태훈_세브란스"
                }
                else{
                    this.name_list += "김태훈_강남세브란스"
                }
            }
            else if(this.get_array[this.get_array.length-1][1] == "서지원"){
                if(this.get_array[this.get_array.length-1][0] == "연세대학교세브란스병원"){
                    this.name_list += "서지원_세브란스"
                }
                else{
                    this.name_list += "서지원_용인세브란스"
                }
            }  
            else{
                this.name_list += this.get_array[this.get_array.length-1][1]
            }
            console.log(this.name_list)
        },
        part_total(){
            var name = $("#cypher").val();
            var nameSplit = name.split(',');
            var str = ""
            console.log(nameSplit.length)
            for(var i = 0; i<nameSplit.length-1; i++){
                str +=  'n.name="'+nameSplit[i]+ '" or '
                console.log(str)
            }
            str += 'n.name="' + nameSplit[nameSplit.length-1] + '"'
            console.log(str)
            var cypher = 'MATCH (n)-[r]->(m) where '+str+' RETURN n,r,m'
            console.log(cypher)
            if (cypher.length > 3) {
                this.viz.renderWithCypher(cypher);
            } else {
                console.log("reload");
                this.viz.reload();
    
            }
        },
        part_paper(){
            var name = $("#cypher").val();            
            var nameSplit = name.split(',');
            var str = ""
            console.log(nameSplit.length)
            for(var i = 0; i<nameSplit.length-1; i++){
                str +=  'n.name="'+nameSplit[i]+ '" or '
                console.log(str)
            }
            str += 'n.name="' + nameSplit[nameSplit.length-1] + '"'
            console.log(str)
            var cypher = 'MATCH (n)-[r:`논문`]->(m) where '+str+' RETURN n,r,m'
            console.log(cypher)
            if (cypher.length > 3) {
                this.viz.renderWithCypher(cypher);
            } else {
                console.log("reload");
                this.viz.reload();
    
            }
        },
        part_test(){
            var name = $("#cypher").val();
            var nameSplit = name.split(',');
            var str = ""
            console.log(nameSplit.length)
            for(var i = 0; i<nameSplit.length-1; i++){
                str +=  'n.name="'+nameSplit[i]+ '" or '
                console.log(str)
            }
            str += 'n.name="' + nameSplit[nameSplit.length-1] + '"'
            console.log(str)
            var cypher = 'MATCH (n)-[r:`임상시험`]->(m) where '+str+' RETURN n,r,m'
            console.log(cypher)
            if (cypher.length > 3) {
                this.viz.renderWithCypher(cypher);
            } else {
                console.log("reload");
                this.viz.reload();
    
            }
        },
        stabilize(){
            this.viz.stabilize();
        },
        draw(){
            var nameSplit = this.name_list.split(',');
            var str = ""
            console.log(nameSplit.length)
            for(var i = 0; i<nameSplit.length-1; i++){
                str +=  'n.name="'+nameSplit[i]+ '" or '
                console.log(str)
            }
            str += 'n.name="' + nameSplit[nameSplit.length-1] + '"'
            console.log(str)
            var cypher = 'MATCH (n)-[r]->(m) where '+str+' RETURN n,r,m'
            console.log(cypher)

            var config = {
				container_id: "viz",
				server_url: "neo4j://7aaa91c2.databases.neo4j.io",
				server_user: "neo4j",
				server_password: "WZvf6UbPjcpBN2YTWui_tzMGX_LBve8L3O8_Z-Rw1Yc",
				labels: {
					//"Character": "name",
					"Doctor": {
						"caption": "name",
						"size": "size",
						"community": "community",
                        //"image":"data:image/png;base64,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",   
                        "title_properties":["name","belong","test","paper","disease_code"]
						//"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
					}
				},
				relationships: {
					"논문": {
						"thickness": "together",//이거 이름 바꾸기
						"caption": "disease_code",
                        //"arrows":true
					},
                    "임상시험": {
						"thickness": "together",
						"caption": "disease_code",
                        //"arrows":true,
					},
				},
                //initial_cypher: "MATCH (n)-[r]->(m) where r.together>50 RETURN n,r,m"
                initial_cypher:cypher
			};

			this.viz = new NeoVis.default(config);
			this.viz.render();
			console.log(this.viz);
        }
    },

}
</script>

<style scoped>
.myDiv{
    width:1200px;
    height: 900px;
}

#viz{
    width: 100%;
    height: 80%;
    border: 1px solid #f1f3f4;
    font: 22pt arial;
}

input{
    border-radius:5px;
    border:1px solid #ccc;
    background-color: #92a4ff;
    width:200px;
    height:50px;
    margin-bottom:10px;
}
#search_name{
    position:relative;
    right:20px;
    top:23px;
    background-color: #f1f3f4;
}
#cypher{
    background-color: #f1f3f4;
}
#choose{
    position:absolute;
    right:50px;
    top:100px;
}

#search{
    position:absolute;
    top:270px;
    right:30px;
}

#stop{
    position:absolute;
    top:30px;
    right:50px;
}
</style>