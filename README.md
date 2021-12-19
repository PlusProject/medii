# mediai+

```
스타트업 기업인 메디아이플러스와 성균관대학교 소프트웨어 학과가 함께 진행한 산학협력프로젝트입니다. 

메디아이플러스는 바이오벤처를 대상으로 임상시험 데이터를 제공해주는 기업으로, 현재 임상시험과 관련된 사업을 진행 중에 있습니다.
```

# 의료진 추천 시스템

이번 프로젝트에서는 심장희귀질병에 관하여 임상시험이 가능한 의료진을 추천해주는 시스템을 만들고자 하였습니다.


![image](https://user-images.githubusercontent.com/66810905/146679402-0e36c9cf-4541-47a3-924e-74508b100345.png)



## Overview 👋

>특정 병원이나 특정 진료과에 속한 모든 의료진을 검색하고 싶을 때
>의료진 개인에 대한 정보를 알아보고자 할 때
>진행하고자 하는 임상시험을 실시할 의료진을 추천받고 싶을 

본 프로젝트는 위와 같은 상황에 대한 솔루션을 제공합니다. 임상시험을 진행하고자 할 때 그 임상시험을 진행할 의료진을 찾는 것은 굉장히 어렵습니다. 한국은 임상시험에 대한 정보 및 의료진에 대한 정보가 흩어져 있어 한 곳에서 살펴볼 수 없기 때문입니다. 

mediai+ 의료진 추천 시스템은 11153개의 임상시험 정보, 3235명의 임상시험 연구진 데이터, 42개 병원의 심장관련 의료진 데이터를 모두 모아 통합된 db를 구축했습니다. 이후 이 데이터를 이용해 검색 시스템과 추천 시스템을 만들어 국내 임상시험 추천 플랫폼 기반을 마련했습니다.

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
