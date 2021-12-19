# web-demo

# On the fit😎

<p align="center">
![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c45f8cda-f3dd-47f3-b3e1-db71bc1e222e/Untitled.png)

</p>
<p align="center">

![npm](https://img.shields.io/badge/npm-7.20.1-blue)
![vue](https://img.shields.io/badge/Vue-2.6.11-green)
![vuetify](https://img.shields.io/badge/Vuetify-2.4.0-9cf)


![issues](https://img.shields.io/github/issues/gyuri2020/codethestudent)
![issues closed](https://img.shields.io/github/issues-closed/gyuri2020/codethestudent)
![pr](https://img.shields.io/github/issues-pr/gyuri2020/codethestudent)
![pr closed](https://img.shields.io/github/issues-pr-closed/gyuri2020/codethestudent)

</p>

대학생들을 위한, 성균관대학생을 위한, 바쁜 율전사람들을 위한,

패션 추천 시스템 "On the fit" 입니다.


## Overview 👋

>율전이는 너무 바빠서 옷을 살 여유가 없습니다. 현재 기온 영하 2도, 아직 여름 반팔티를 입고 있습니다. 어차피 사 봤자 도서관가는 것과 과제하는 것이 전부인데 무슨 의미인가 싶습니다. 그런데 어느날 학과 친구에게 연락이 왔습니다. 코로나-19 거리두기도 완화됐으니 종강파티를 하자고 합니다. 
>
>소식을 들은 율전이는 급하게 겨울 옷을 구매하려고 인터넷 쇼핑몰에 방문하였습니다. 하지만 평소 패션에 관심을 끊고 살던 율전이는 어떤 브랜드를 신뢰해야 할 지, 요즘 어떤 스타일이 유행하는 지 전혀 모릅니다.

본 팀 codethestudent는 위와 같은 상황에 대한 솔루션을 제공합니다. 인터넷 쇼핑몰은 다양한 층의 사람들을 상대해야 하므로 패션에 관심이 없는 율전이 같은 사람들에게는 어려울 수 있습니다. 

On the fit은 오직 20대 남/여의 검색 트랜드를 분석하여 상품들을 추천해줍니다. 게다가 카테고리를 범용적으로 나눈 것이 아닌, 현재 20대 남/여에게 유행하는 패션 아이템을 선정하여 구성하였습니다.

## Installation ⚙

1. repo 받아오기
```
# git이 선행으로 깔려있어야 합니다.
git clone https://github.com/gyuri2020/codethestudent
```
2. dependencies 설치
```
cd codethestudent
npm install
```
3. 로컬 서버 열기
```
npm run serve
```

## How to use 🤔

1. [On the fit](https://gyuri2020.github.io/codethestudent/)에 접속합니다.
2. 카테고리를 선택합니다.
3. 맘에드는 상품을 파악합니다.

![image](https://user-images.githubusercontent.com/79851762/143767170-753c4b1e-0b10-4341-8d72-d26470db63af.png)

![image](https://user-images.githubusercontent.com/79851762/143767230-81e40394-8d61-44f4-bbc2-1e1fea6422e6.png)

![image](https://user-images.githubusercontent.com/79851762/143767263-f7cabc58-0caf-46a1-afb6-ee3692e41ca1.png)
  
## Contribute Guide 🚩

+ PR을 올려주세요. 코드리뷰 후에 merge&rebase 하도록 합니다.
+ 커밋을 단위별로 올려주세요. [가이드](https://tech.10000lab.xyz/git/git-commit-discipline.html)를 참고해주세요.
+ 이슈 위주로 Task를 관리합니다. 이슈를 활용해 주세요.
+ 호스팅은 `release`브랜치로 이루어집니다. 서버 환경처럼 테스팅할 방법은 제공하지 않으며, 후에 docker를 통해 API코드와(후에 backend로 확장할 것) 함께제공할 예정입니다.
  + `github action`기능으로 `gh-pages'와 함께 deployment를 담당하고 있습니다.
+ 네이버 쇼핑 검색 API를 사용합니다.
  
## API 🌉

- [네이버 쇼핑 검색](https://developers.naver.com/products/service-api/search/search.md)
  - 유저가 선택한 카테고리를 인풋으로 api를 호출합니다.
  - 선택된 카테고리에 해당하는 상품 정보를 가져와 렌더링합니다.

back-end로는 [AWS lambda](https://aws.amazon.com/ko/lambda/)를 사용하였습니다. 호출할 API의 개수가 적기 때문에 따로 back-end서버를 구축하지 않았습니다. AWS lambda를 통해 API를 연결하고, 추가로 CORS이슈까지 해결합니다.

*코드는 이에 대한 깃허브 repo에 없습니다. 후에 back-end서버를 구축하게 될 때, 추가할 예정입니다.*

## Members

이규리 [@gyuri2020](https://github.com/gyuri2020)
> 성균관대학교 소프트웨어학과 20학번
> 
> Contact: lj01081512@gmail.com

이윤성 [@anzanda](https://github.com/anzanda)
> 성균관대학교 소프트웨어학과 20학번
> 
> Contact: tjd8899@gmail.com

## Demo

Here is [link](https://youtu.be/WiSgzTOSgPI)😳
