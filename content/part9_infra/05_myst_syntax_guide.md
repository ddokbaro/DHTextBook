---
title: MyST Markdown 표준 문법 가이드
subtitle: 디지털 인문학 교과서 집필 규칙
---

이 문서는 Jupyter Book의 표준 문법인 **MyST(Markedly Structured Text)**의 핵심 사용법을 정리한 교육용 문서입니다. 일반적인 마크다운 문법에 학술적인 글쓰기를 위한 기능(각주, 인용, 수식, 상호 참조 등)이 추가된 형태입니다.

## 1. 텍스트 강조 (Text Formatting)

기본적인 텍스트 강조는 일반 마크다운과 동일합니다.

* **굵게**: `**굵은 텍스트**` → **굵은 텍스트**
* *기울임*: `*기울임 텍스트*` → *기울임 텍스트*
* `인라인 코드`: `` `코드` `` → `코드`
* ~~취소선~~: `~~취소선~~` → ~~취소선~~

## 2. 블록 인용 및 경고창 (Admonitions)

교과서나 기술 문서에서 중요한 내용을 강조할 때 사용하는 박스 형태의 문법입니다. `:::{type}` 형식을 사용합니다.

### 기본 노트

```md
:::{note}
이곳에 노트 내용을 작성합니다.
보충 설명이나 참고 사항을 적을 때 유용합니다.
:::
```

### 경고 (Warning)

```md
:::{warning}
주의가 필요한 내용은 warning을 사용합니다.
:::
```

### 팁 (Tip)

```md
:::{tip}
유용한 팁이나 지름길을 안내할 때 사용합니다.
:::
```

### 제목이 있는 박스 (Custom Admonition)

```md
:::{admonition} 여기에는 제목이 들어갑니다
:class: seealso

본문 내용은 여기에 작성합니다. `seealso`, `tip`, `warning` 등 클래스를 지정하여 색상을 바꿀 수 있습니다.
:::
```

## 3. 이미지와 그림 (Figures)

단순 이미지 삽입을 넘어, 캡션(설명)을 달고 크기를 조절하려면 `{figure}` 지시어를 사용합니다.

```md
:::{figure} [https://mystmd.org/images/logo.png](https://mystmd.org/images/logo.png)
:name: my-figure-label
:width: 200px
:align: center

여기에 이미지 캡션(설명)을 적습니다.
:::
```

* `:name:`: 나중에 본문에서 이 그림을 참조할 때 사용하는 ID입니다.
* `:width:`: 이미지의 너비를 지정합니다 (px 또는 %).
* `:align:`: 정렬 방식 (left, center, right).

## 4. 코드 블록 (Code Blocks)

프로그래밍 코드를 작성할 때는 언어를 지정하고, 필요시 줄 번호나 제목을 붙일 수 있습니다.

```python
def hello_world():
    print("Hello, Digital Humanities!")
```

옵션을 추가하려면 다음과 같이 작성합니다.

````md
```python
:linenos:
:caption: 파이썬 예제 코드

def hello_world():
    print("Hello, Digital Humanities!")
```
````

## 5. 수식 (Math & LaTeX)

학술적인 수식은 LaTeX 문법을 사용하여 표현합니다.

### 인라인 수식 (문장 중간)
문장 중간에 $E = mc^2$ 처럼 수식을 넣으려면 `$` 기호를 사용합니다.
* 입력: `$E = mc^2$`

### 블록 수식 (별도 문단)
수식을 가운데 정렬하여 크게 보여주려면 `$$` 또는 `{math}` 지시어를 사용합니다.

```md
$$
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

수식에 번호를 붙여서 참조하려면 다음과 같이 씁니다.

```md
:::{math}
:label: my-equation

x = \frac{1}{2} a t^2 + v_0 t + x_0
:::
```

## 6. 상호 참조 (Cross-Referencing)

문서 내의 다른 챕터, 그림, 수식 등을 링크할 때 사용합니다. 페이지 번호가 바뀌어도 링크가 유지되므로 매우 중요합니다.

### 섹션(제목) 참조하기
참조하고 싶은 제목 바로 위에 라벨을 붙입니다.

```md
(section-label)=
## 2. 데이터 분석 방법
```

다른 곳에서 위 섹션을 링크하려면:
* 입력: `2장 {ref}`section-label` 내용을 참고하세요.`
* 출력: 2장 **2. 데이터 분석 방법** 내용을 참고하세요.

### 그림/수식 참조하기
그림이나 수식에 `:name:` 또는 `:label:`을 붙였다면 `{ref}` 대신 `{numref}`를 써서 "그림 1", "식 2" 처럼 번호로 참조할 수 있습니다.

* 입력: `{numref}`my-figure-label`을 보세요.`
* 출력: **그림 1**을 보세요.

## 7. 각주 (Footnotes)

본문 내용에 부가 설명을 달 때 사용합니다.

```md
디지털 인문학[^dh]은 인문학 연구에 디지털 기술을 접목한 분야입니다.

[^dh]: Digital Humanities의 약자.
```

## 8. 탭 (Tab Set)

여러 언어의 코드나, 다양한 옵션을 탭으로 보여주고 싶을 때 사용합니다.

```md
::::{tab-set}

:::{tab-item} Python
print("Hello Python")
:::

:::{tab-item} JavaScript
console.log("Hello JS");
:::

::::
```

---

**더 자세한 내용 참고:**
* [MyST 공식 문서 (영문)](https://mystmd.org/guide)
* [Jupyter Book 갤러리](https://executablebooks.org/en/latest/gallery/)