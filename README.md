# NeoNews 너뉴스 v1.0 

![제목 추가 (4) (1)](https://user-images.githubusercontent.com/64240637/135853851-bcff88fb-05e5-4848-b4d6-22f8b95b7157.png)

<br>

## 목차 | Contents
1. [너뉴스 소개](https://github.com/Neo-News/Neo-News/tree/develop#-%EB%84%88%EB%89%B4%EC%8A%A4-%EC%86%8C%EA%B0%9C)   
2. [개요](https://github.com/Neo-News/Neo-News/tree/develop#-%EA%B0%9C%EC%9A%94)   
3. [요구사항 및 업무 분배](https://github.com/Neo-News/Neo-News/tree/develop#-%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD-%EB%B0%8F-%EC%97%85%EB%AC%B4-%EB%B6%84%EB%B0%B0)   
4. [주요 기능](https://github.com/Neo-News/Neo-News/tree/develop#-%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5)     
5. [ERD](https://github.com/Neo-News/Neo-News/tree/develop#-erd)   
6. [History](https://github.com/Neo-News/Neo-News/tree/develop#-history)   

<br>

## 📚 너뉴스 소개
- 원하는/관심있는 기사를 찾기 위해 포털사이트 속에서 여러번 클릭을 했던 귀찮은 경험을 했었습니다. 
- 기사와 동시에 화면에 뜨는 여러개의 광고배너, 광고글을 실수로 누르게 되는 경우도 꽤 많았습니다. 
- 관심있는 이슈를 손쉽게 모아보고 싶은 생각도 했었습니다.

 이러한 불편함은 없애고  __매일매일 쏟아지는 뉴스 기사 속에서 내가 원하는 기사의 카테고리를 직접 선택하고 관심 키워드를 직접 입력하여 오로지 기사만을 볼 수 있는 나만의 뉴스공간의 웹/앱사이트를 만들게 되었습니다.__

<br>

## 📌 개요

- 기간 : 2021.08.01 ~ 2021.09.07
- 팀원
  - Back-end & Front-end : [오지윤]()
  - Back-end & Front-end : [손희정]()
  - BackEnd 개발자 2명이 협업하여 프로젝트를 진행하였습니다. 

<br>

## ➗ 요구사항 및 업무 분배
팀 노션을 이용해 요구사항을 작성하였고 새로운 기술에 대한 정보를 공유하였습니다. github의 [issue](https://github.com/Neo-News/Neo-News/issues)와 [projects](https://github.com/Neo-News/Neo-News/projects)를 활용해 개발 진행사항을 공유하였으며 개발과정에서 발생한 이슈와 이슈 해결과정 등을 공유했습니다.

![요구사항](https://user-images.githubusercontent.com/64240637/135860718-f99ed25f-be96-4793-a210-169727184138.png)

<br>

## 🌟 주요 기능
### 1. 로그인
  - 카카오 계정 소셜 로그인 방식을 사용합니다.   
  - 일반 로그인 방식을 사용합니다. 
  - 비밀번호를 잊어버렸을 경우 비밀번호를 찾을 수 있습니다.   
### 2. 회원가입
  - 일반 회원가입시 이메일 인증을 통해 유저를 인증합니다.
  - celery를 통해 이메일 인증시 로딩시간을 단축 시켜줍니다.
### 2. 기사 필터
  - 스크래핑된 기사를 보여줍니다.   
  - 카테고리별로 기사를 나누어 볼 수 있습니다.
  - 키워드별로 원하는 기사만을 모아 볼 수 있습니다.
  - 한 페이지에 20개씩의 기사를 보여줍니다. 
### 3. 세부 기사
  - 카카오톡 공유하기를 통해 기사를 공유할 수 있습니다.
  - 마음에 드는 기사에 좋아요를 남길 수 있습니다.
  - 자신의 의견등을 기사의 댓글/대댓글에 남길 수 있습니다.
### 4. 설정페이지
  - 언론사를 직접 선택/해제하여 언론사에 대한 기사를 받아 볼 수 있습니다.
  - 키워드를 입력/삭제하여 키워드에 관련된 기사를 받아 볼 수 있습니다.
  - 카테고리를 선택/해제하여 카테고리에 관련된 기사를 받아볼 수 있습니다.

### 5. 마이페이지
- 자신의 프로필 이미지나 닉네임을 변경 할 수 있습니다.
- 자신이 댓글을 단 기사를 확인할 수 있습니다.
- 자신이 좋아요 한 기사를 확인할 수 있습니다.
- 사이트를 탈퇴 할 수 있습니다.    

### 6. 반응형 앱
- 사이트에 대한 유저의 접근성을 고려하여 반응형 앱으로 구현하였습니다.

<br>

## 🔖 ERD
![erd](https://user-images.githubusercontent.com/64240637/135862011-9edec5b8-06f9-42cb-9a6f-42f60b2fe01f.png)

<br>

## 🐥 History
### [WIKI]()    
### [v2.0]()
