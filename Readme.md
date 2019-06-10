# Demo Block chain

>for CSE4115

## Diagram
![Diagram](./diagram.png)

## Getting Started

### Prerequisties
```
virtualenv $(venv name)
```

### installing
```
pip install requirements.txt
```

## Problem Description
[description](./Description.md)

## Project Check List

1.	블록체인 노드가 5개가 다 접속 확인이 가능한가?  
2.	두개 이상의 노드가 Miner인가  
3.	각각의 노드는 데이터 송수신이 가능한가?  
4.	각각의 노드는 개인키, 공개키를 가지고 있는가?  
5.	트랜잭션 형태는 { From, to, data, timestamp } 형태인가?  
6.	트랜잭션은 개인키로 암호화 하여 공개키로 검증이 가능한가?  
7.	블록에는 {index, timestamp, previous block hash, transaction_list, nonce, block producer}가 포함되어 있는가?  
8.	Transaction pool 을 통해서 개인키로 암호화된 transaction이 확인 가능한가?  
9.	악의적인 Transaction이 폐기 되는 과정이 확인 가능한가?  
10.	Mining 과정을 볼 수 있는가?  
11.	트랜잭션 10개마다 Mining이 시작이 되는가?  
12.	트랜잭션 전파 과정이 확인 가능한가?  
13.	블록 전파 과정이 확인 가능한가?  
14.	GUI를 통해 모든 과정을 확인 할 수 있는가?  
