---
title: "XML에서 데이터 과학으로의 연결: Pandas와 SNA"
description: "lxml로 추출한 다차원 TEI 데이터를 2차원 Pandas 데이터프레임으로 변환하고, 인물 관계망 분석(SNA)을 위한 노드와 엣지 리스트를 구축하는 파이프라인 실무"
---

# XML에서 데이터 과학으로의 연결: Pandas와 SNA

지금까지 우리는 텍스트를 논리적으로 구조화(TEI)하고, `lxml`의 `iterparse`와 XPath를 활용해 대용량 문헌에서 원하는 정보만 메모리 초과 없이 핀셋처럼 추출해 내는 정보공학적 기술을 마스터했습니다. 

그러나 컴퓨터 공학의 관점에서 XML은 데이터를 `"**저장하고 교환하기 위한 최적의 그릇**"`일 뿐, 통계를 내거나 머신러닝(Machine Learning) 모델을 돌리기 위한 구조는 아닙니다. 현대 데이터 과학(Data Science) 및 자연어 처리(NLP) 생태계는 2차원의 표(Table) 구조나 행렬(Matrix) 구조를 요구합니다. 

이 장에서는 복잡한 계층을 가진 XML 트리 데이터를 파이썬의 `"**Pandas 데이터프레임(DataFrame)**"`으로 완벽하게 변환하고, 더 나아가 역사 인물들의 사회 연결망 분석(SNA, Social Network Analysis)을 위한 `"**노드-엣지(Node-Edge) 리스트**"`를 추출하는 궁극의 실무 파이프라인을 구축합니다.

## 1. 딕셔너리 리스트(List of Dicts): 완벽한 징검다리

다차원 구조의 XML을 Pandas 데이터프레임으로 변환할 때, 요소를 찾을 때마다 한 줄씩 데이터프레임에 밀어 넣는(Append) 방식은 컴퓨터의 연산 속도를 극도로 저하시키는 비효율적인 방식입니다. 

효율성을 극대화하기 위해서는 XML을 훑으면서 추출한 데이터를 파이썬의 `"**딕셔너리(Dictionary)들을 담은 리스트**"`로 먼저 1차 가공하는 것이 정석입니다.



가상의 `"**종묘배향공신**"` TEI 인물 사전 데이터를 예로 들어보겠습니다.

```python
from lxml import etree
import pandas as pd

# TEI 네임스페이스 통제
ns = {'tei': '[http://www.tei-c.org/ns/1.0](http://www.tei-c.org/ns/1.0)'}
tree = etree.parse('jongmyo_meritorious_retainers.xml')

# 1. 데이터를 담을 빈 리스트 생성 (징검다리 역할)
person_data_list = []

# 2. 모든 인물 정보(<person>) 순회 및 추출
for person in tree.xpath('//tei:person', namespaces=ns):
    
    # 각 인물의 고유 ID 및 기본 메타데이터 추출
    pid = person.get('{[http://www.w3.org/XML/1998/namespace](http://www.w3.org/XML/1998/namespace)}id')
    name = person.findtext('.//tei:persName', namespaces=ns)
    birth_year = person.findtext('.//tei:birth', namespaces=ns)
    status = person.findtext('.//tei:state[@type="status"]/tei:desc', namespaces=ns)
    
    # 3. 추출한 데이터를 딕셔너리로 묶어 리스트에 추가
    person_dict = {
        'PersonID': pid,
        'Name': name,
        'BirthYear': int(birth_year) if birth_year else None,
        'Status': status
    }
    person_data_list.append(person_dict)
```

## 2. Pandas 데이터프레임 변환과 정제

위에서 구축한 `person_data_list`를 Pandas 라이브러리에 넘겨주면, 단 한 줄의 코드로 완벽한 형태의 2차원 데이터프레임이 생성됩니다.

```python
# 4. 리스트를 Pandas DataFrame으로 변환
df_persons = pd.DataFrame(person_data_list)

# 5. 데이터 구조 확인 및 결측치(NaN) 처리
print(df_persons.head())
print(df_persons.info())

# 결측치(생년 미상 등)를 특정 값으로 채우거나 제거하는 정제 작업
df_persons['BirthYear'].fillna('Unknown', inplace=True)
```

이제 이 `df_persons` 객체를 통해 "특정 신분(Status)을 가진 공신의 수"를 통계 내거나, CSV/Excel 파일로 즉각 추출하여 연구 보고서에 활용할 수 있습니다. 

## 3. 시맨틱 관계망 분석(SNA)을 위한 데이터 추출 ★

인문학에서 종묘배향공신과 같은 역사 인물들의 학연, 지연, 정치적 대립 관계를 파악하는 것은 단일 인물의 생몰년을 아는 것보다 훨씬 거대한 통찰을 제공합니다. 네트워크 분석(SNA) 도구인 `NetworkX`나 시각화 프로그램인 `Gephi`를 활용하려면, 데이터가 단순히 개인의 목록을 넘어 `"**노드(Node: 점)**"`와 `"**엣지(Edge: 선)**"`의 관계로 분리되어야 합니다.



TEI 가이드라인에서 인물 간의 관계는 주로 `<listRelation>` 내의 `<relation>` 요소로 마크업됩니다. 이를 파이썬으로 뜯어내어 관계성(Edge) 데이터프레임으로 독립시키는 실무 코드는 다음과 같습니다.

**[TEI 관계성 마크업 예시]**
```xml
<listRelation>
    <relation name="teacher_of" active="#person_A" passive="#person_B"/>
    <relation name="political_enemy" active="#person_A" passive="#person_C" mutual="#person_A #person_C"/>
</listRelation>
```

**[엣지 리스트 파이썬 추출 코드]**
```python
edge_data_list = []

# 모든 <relation> 요소를 순회하며 발신자(active)와 수신자(passive) 추출
for rel in tree.xpath('//tei:relation', namespaces=ns):
    rel_type = rel.get('name')
    active_node = rel.get('active').replace('#', '') if rel.get('active') else None
    passive_node = rel.get('passive').replace('#', '') if rel.get('passive') else None
    
    # 상호 관계(mutual)인 경우 양방향 엣지를 위해 분리 처리
    mutual_nodes = rel.get('mutual')
    
    if active_node and passive_node:
        edge_data_list.append({
            'Source': active_node,
            'Target': passive_node,
            'RelationType': rel_type,
            'Weight': 1  # 연결 강도
        })
    elif mutual_nodes:
        nodes = mutual_nodes.split()
        if len(nodes) == 2:
            # A와 B가 서로 적대 관계인 경우 등 상호작용 명시
            edge_data_list.append({'Source': nodes[0].replace('#',''), 'Target': nodes[1].replace('#',''), 'RelationType': rel_type, 'Weight': 1})
            edge_data_list.append({'Source': nodes[1].replace('#',''), 'Target': nodes[0].replace('#',''), 'RelationType': rel_type, 'Weight': 1})

# 관계 데이터프레임(Edge List) 생성
df_edges = pd.DataFrame(edge_data_list)

# 네트워크 분석 프로그램용으로 CSV 내보내기
df_edges.to_csv('jongmyo_edges.csv', index=False, encoding='utf-8-sig')
df_persons.to_csv('jongmyo_nodes.csv', index=False, encoding='utf-8-sig')
```

이 추출 방식을 통해 생성된 `jongmyo_nodes.csv`와 `jongmyo_edges.csv` 두 개의 파일은 텍스트 인코딩 작업이 거대한 `"**지식 그래프(Knowledge Graph)**"`로 개화하는 궁극적인 결과물입니다. 파이썬의 `NetworkX` 라이브러리에 이 데이터를 밀어 넣는 순간, 기계는 공신들 사이의 숨겨진 파벌과 가장 영향력 있었던 핵심 허브(Hub) 인물을 수학적으로 계산해 냅니다.

결론적으로, 디지털 문헌학에서 마크업(XML/TEI)은 과거를 기록하는 완벽한 아카이빙 행위이고, 파이썬과 데이터 과학(Pandas/SNA)은 그 과거의 기록을 해체하여 새로운 미래의 지식을 창발시키는 연금술입니다. 전자문서와 하이퍼텍스트의 철학적, 기술적 융합은 바로 이 지점에서 찬란하게 완성됩니다.

:::{seealso} 📖 참고문헌
* **Wes McKinney.** <Python for Data Analysis>. O'Reilly.
* **TEI Consortium.** <TEI P5 Guidelines: Names, Dates, People, and Places>.
:::