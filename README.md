# mediai+

```
스타트업 기업인 메디아이플러스와 성균관대학교 소프트웨어 학과가 함께 진행한 산학협력프로젝트입니다. 

메디아이플러스는 바이오벤처를 대상으로 임상시험 데이터를 제공해주는 기업으로, 
현재 임상시험과 관련된 사업을 진행 중에 있습니다.
```

# 의료진 추천 시스템

이번 프로젝트에서는 심장희귀질병에 관하여 임상시험이 가능한 의료진을 추천해주는 시스템을 만들고자 하였습니다.


![image](https://user-images.githubusercontent.com/66810905/146679402-0e36c9cf-4541-47a3-924e-74508b100345.png)



## Overview 👋

>특정 병원이나 특정 진료과에 속한 모든 의료진을 검색하고 싶을 때
>
>의료진 개인에 대한 정보를 알아보고자 할 때
>
>진행하고자 하는 임상시험을 실시할 의료진을 추천받고 싶을 때 

본 프로젝트는 위와 같은 상황에 대한 솔루션을 제공합니다. 임상시험을 진행하고자 할 때 그 임상시험을 진행할 의료진을 찾는 것은 굉장히 어렵습니다. 한국은 임상시험에 대한 정보 및 의료진에 대한 정보가 흩어져 있어 한 곳에서 살펴볼 수 없기 때문입니다. 

mediai+ 의료진 추천 시스템은 11153개의 임상시험 정보, 3235명의 임상시험 연구진 데이터, 42개 병원의 심장관련 의료진 데이터를 모두 모아 통합된 db를 구축했습니다. 이후 이 데이터를 이용해 검색 시스템과 추천 시스템을 만들어 국내 임상시험 추천 플랫폼 기반을 마련했습니다.

## Installation ⚙

1. repo 받아오기
```
# git이 선행으로 깔려있어야 합니다.
git clone https://github.com/PlusProject/web-demo.git
```
2. dependencies 설치
```
<backend dependencies>
cd web-demo
cd backend
가상 환경 및 기타 실행에 필요한 library를 pip를 이용해 설치해줍니다.
```
```
<frontend dependencies>
cd web-demo
cd frontend
npm install
```

3. 로컬 서버 열기
```
<backend local server>
cd backend
python manage.py runserver

<frontend local server>
cd frontend
npm run serve

```

## How to use 🤔

1. [mediai+](http://3.35.243.113/)에 접속합니다.
2. 홈페이지에서 실행하고자 하는 임상시험 질병 코드를 입력해주세요.
3. 그러면 그 질병 코드와 관련된 의료진이 의료진의 질병 전문성, 영향력, 저명도에 점수를 매겨 추천되게 됩니다.
4. 오른쪽 상단에 현재 추천방식을 나타내주는 버튼이 있습니다. 기본은 paper impact를 고려한 추천으로 설정되어 있고, 해당 버튼을 누르면 다른 추천 결과(중분류를 고려한 추천)가 보여집니다.

![image](https://user-images.githubusercontent.com/66810905/146680544-fe95348f-93dc-4722-ac1a-c74f509fe699.png)


![image](https://user-images.githubusercontent.com/66810905/146680309-85e891cd-8ed7-48be-9db4-8d914daffd32.png)


![image](https://user-images.githubusercontent.com/66810905/146680379-69bca297-2679-42d8-b6b5-cdf53b4647b5.png)

  
## Contribute Guide 🚩

+ PR을 올려주세요. 코드리뷰 후에 merge&rebase 하도록 합니다.
+ 커밋을 단위별로 올려주세요. [가이드](https://tech.10000lab.xyz/git/git-commit-discipline.html)를 참고해주세요.
+ 이슈 위주로 Task를 관리합니다. 이슈를 활용해 주세요.
+ ACM API를 사용합니다.
+ ACM API는 사용할 때마다 돈이 청구되니 사용하실 때 유의하시길 바랍니다.
  

## Members

이규리
> 성균관대학교 소프트웨어학과 20학번
> 
>

지예성
> 성균관대학교 소프트웨어학과 19학번
> 
> 

남동완
> 성균관대학교 소프트웨어학과 20학번
> 


이현민
> 성균관대학교 소프트웨어학과 20학번
> 
> 

