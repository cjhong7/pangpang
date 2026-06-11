# -*- coding: utf-8 -*-
"""
한글 팡팡 게임 사용자 설명서 — 고품질 PDF 생성
참조 스타일: 도전 四字成語 사용자 설명서
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, PageBreak,
    NextPageTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# ─── 폰트 등록 ──────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('MG',  r'C:\Windows\Fonts\malgun.ttf'))
pdfmetrics.registerFont(TTFont('MGB', r'C:\Windows\Fonts\malgunbd.ttf'))
pdfmetrics.registerFont(TTFont('CS',  r'C:\Windows\Fonts\consola.ttf'))

W, H   = A4
COL_W  = W - 4 * cm    # 본문 콘텐츠 너비

# ─── 색상 ───────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor('#0d1b4b')
CH_BG  = colors.HexColor('#1a3a6b')
BLUE   = colors.HexColor('#1565c0')
LBLUE  = colors.HexColor('#dbeafe')
LGRN   = colors.HexColor('#dcfce7')
LYEL   = colors.HexColor('#fef9c3')
LRED   = colors.HexColor('#fee2e2')
ALT    = colors.HexColor('#e8eaf6')
TEXT   = colors.HexColor('#1a1a1a')
LGRAY  = colors.HexColor('#f5f5f5')
DGRAY  = colors.HexColor('#555555')
RED    = colors.HexColor('#b71c1c')
GREEN  = colors.HexColor('#1b5e20')
ORANGE = colors.HexColor('#c25b00')

# ─── 텍스트 도우미 ──────────────────────────────────────────────────────────
def safe(text):
    t = str(text)
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def safe_nl(text):
    t = str(text)
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return t.replace('\n', '<br/>')

def b(text):
    return '<font name="MGB">{}</font>'.format(safe(text))

def c(text):
    return '<font name="CS" size="8.5" color="#c0392b">{}</font>'.format(safe(text))

# ─── 스타일 ─────────────────────────────────────────────────────────────────
def build_styles():
    S = {}
    # 표지
    S['cov_title']  = ParagraphStyle('cov_title', fontName='MGB', fontSize=38, leading=52,
                                      textColor=colors.white, alignment=TA_CENTER)
    S['cov_sub']    = ParagraphStyle('cov_sub',   fontName='MG',  fontSize=15, leading=22,
                                      textColor=colors.HexColor('#b0c4de'), alignment=TA_CENTER)
    S['cov_th']     = ParagraphStyle('cov_th',    fontName='MGB', fontSize=9,  leading=13,
                                      textColor=colors.white, alignment=TA_CENTER)
    S['cov_td']     = ParagraphStyle('cov_td',    fontName='MG',  fontSize=9,  leading=13,
                                      textColor=colors.HexColor('#ddeeff'), alignment=TA_CENTER)
    S['cov_toc_h']  = ParagraphStyle('cov_toc_h', fontName='MGB', fontSize=9,  leading=13,
                                      textColor=colors.white, alignment=TA_CENTER)
    S['cov_toc_ch'] = ParagraphStyle('cov_toc_ch',fontName='MGB', fontSize=8.5,leading=13,
                                      textColor=colors.HexColor('#7fb0e8'), alignment=TA_CENTER)
    S['cov_toc_t']  = ParagraphStyle('cov_toc_t', fontName='MG',  fontSize=8.5,leading=13,
                                      textColor=colors.HexColor('#cce0ff'), alignment=TA_LEFT)
    # 장 헤더
    S['ch_hdr'] = ParagraphStyle('ch_hdr', fontName='MGB', fontSize=14, leading=20,
                                  textColor=colors.white)
    # 본문 헤더
    S['h2']     = ParagraphStyle('h2',     fontName='MGB', fontSize=11, leading=18,
                                  textColor=BLUE,  spaceBefore=12, spaceAfter=3)
    S['h3']     = ParagraphStyle('h3',     fontName='MGB', fontSize=10, leading=16,
                                  textColor=colors.HexColor('#37474f'), spaceBefore=8,
                                  spaceAfter=2, leftIndent=4)
    # 본문
    S['body']      = ParagraphStyle('body',      fontName='MG',  fontSize=9.5, leading=16,
                                     textColor=TEXT, spaceBefore=2, spaceAfter=2,
                                     alignment=TA_JUSTIFY)
    S['bullet']    = ParagraphStyle('bullet',    fontName='MG',  fontSize=9.5, leading=16,
                                     textColor=TEXT, spaceBefore=1, spaceAfter=1,
                                     leftIndent=14, firstLineIndent=-10)
    S['num']       = ParagraphStyle('num',       fontName='MG',  fontSize=9.5, leading=16,
                                     textColor=TEXT, spaceBefore=1, spaceAfter=1,
                                     leftIndent=18, firstLineIndent=-14)
    # 박스
    S['note']   = ParagraphStyle('note',   fontName='MG',  fontSize=9, leading=15, textColor=GREEN)
    S['warn']   = ParagraphStyle('warn',   fontName='MG',  fontSize=9, leading=15, textColor=ORANGE)
    S['info']   = ParagraphStyle('info',   fontName='MG',  fontSize=9, leading=15,
                                  textColor=colors.HexColor('#0d47a1'))
    S['impt']   = ParagraphStyle('impt',   fontName='MGB', fontSize=9, leading=15, textColor=RED)
    # 테이블
    S['th']     = ParagraphStyle('th',     fontName='MGB', fontSize=9, leading=13,
                                  textColor=colors.white, alignment=TA_CENTER)
    S['td']     = ParagraphStyle('td',     fontName='MG',  fontSize=9, leading=14, textColor=TEXT)
    S['td_c']   = ParagraphStyle('td_c',   fontName='MG',  fontSize=9, leading=14,
                                  textColor=TEXT, alignment=TA_CENTER)
    S['td_code']= ParagraphStyle('td_code',fontName='CS',  fontSize=8.5, leading=14,
                                  textColor=colors.HexColor('#c0392b'))
    # Quick Start
    S['qs_num'] = ParagraphStyle('qs_num', fontName='MGB', fontSize=11, leading=17,
                                  textColor=BLUE, spaceBefore=12, spaceAfter=3)
    S['qs_body']= ParagraphStyle('qs_body',fontName='MG',  fontSize=9.5, leading=16,
                                  textColor=TEXT, spaceBefore=2, leftIndent=14)
    return S


# ─── 레이아웃 헬퍼 ──────────────────────────────────────────────────────────
def sp(h=6):
    return Spacer(1, h)

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cccccc'),
                      spaceBefore=4, spaceAfter=4)

def ch_hdr(text, S):
    data = [[Paragraph(safe(text), S['ch_hdr'])]]
    t = Table(data, colWidths=[COL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), CH_BG),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
    ]))
    return t

def note_box(text, S):
    data = [[Paragraph(safe_nl(text), S['note'])]]
    t = Table(data, colWidths=[COL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LGRN),
        ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#a8d5b5')),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def warn_box(text, S):
    data = [[Paragraph(safe_nl(text), S['warn'])]]
    t = Table(data, colWidths=[COL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LYEL),
        ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#f0c040')),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def info_box(text, S):
    data = [[Paragraph(safe_nl(text), S['info'])]]
    t = Table(data, colWidths=[COL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LBLUE),
        ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#90caf9')),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def imp_box(text, S):
    data = [[Paragraph(safe_nl(text), S['impt'])]]
    t = Table(data, colWidths=[COL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LRED),
        ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#ef9a9a')),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def make_table(S, headers, rows, col_widths=None, center_cols=None):
    if col_widths is None:
        col_widths = [COL_W / len(headers)] * len(headers)
    center_cols = set(center_cols or [])
    data = [[Paragraph(safe(h), S['th']) for h in headers]]
    for row in rows:
        r = []
        for ci, cell in enumerate(row):
            sty = S['td_c'] if ci in center_cols else S['td']
            r.append(Paragraph(safe_nl(str(cell)), sty))
        data.append(r)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  BLUE),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, ALT]),
        ('GRID',          (0,0), (-1,-1), 0.4, colors.HexColor('#bdbdbd')),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 7),
        ('RIGHTPADDING',  (0,0), (-1,-1), 7),
        ('LINEBELOW',     (0,0), (-1,0),  1.2, colors.HexColor('#0d47a1')),
    ]))
    return t

def bul(text, S):
    return Paragraph('- ' + safe_nl(text), S['bullet'])

def nm(n, text, S):
    return Paragraph('{}. '.format(n) + safe_nl(text), S['num'])

def body(text, S):
    return Paragraph(safe_nl(text), S['body'])

def fmt(text, S, style='body'):
    return Paragraph(text, S[style])


# ─── 페이지 콜백 ────────────────────────────────────────────────────────────
def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # 상단 진한 스트라이프
    canvas.setFillColor(colors.HexColor('#070f2e'))
    canvas.rect(0, H - 3.5*cm, W, 3.5*cm, fill=1, stroke=0)
    # 하단 진한 스트라이프
    canvas.rect(0, 0, W, 2.2*cm, fill=1, stroke=0)
    # 구분선
    canvas.setStrokeColor(colors.HexColor('#3355aa'))
    canvas.setLineWidth(1.0)
    canvas.line(2*cm, H - 3.5*cm, W - 2*cm, H - 3.5*cm)
    canvas.line(2*cm, 2.2*cm, W - 2*cm, 2.2*cm)
    # 상단 보조 문구
    canvas.setFont('MG', 8.5)
    canvas.setFillColor(colors.HexColor('#7799cc'))
    canvas.drawCentredString(W/2, H - 2.1*cm,
        '초등학교 한글 교육용 웹게임  |  교실 TV / 터치스크린 / 웹브라우저')
    # 하단 제작 정보
    canvas.setFont('MG', 8)
    canvas.setFillColor(colors.HexColor('#4466aa'))
    canvas.drawCentredString(W/2, 1.0*cm, '2026년 6월   제작: Claude (Anthropic) x cjhong7')
    canvas.restoreState()

def draw_body(canvas, doc):
    canvas.saveState()
    # 헤더
    canvas.setFont('MG', 8)
    canvas.setFillColor(DGRAY)
    canvas.drawString(2*cm, H - 1.5*cm, '한글 팡팡 게임 사용자 설명서')
    canvas.drawRightString(W - 2*cm, H - 1.5*cm, 'v2026.06')
    canvas.setStrokeColor(colors.HexColor('#cccccc'))
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, H - 1.8*cm, W - 2*cm, H - 1.8*cm)
    # 푸터 페이지 번호 (표지 1페이지 제외)
    pn = canvas.getPageNumber() - 1
    canvas.setFont('MG', 8.5)
    canvas.setFillColor(DGRAY)
    canvas.drawCentredString(W/2, 1.4*cm, '--  {}  --'.format(pn))
    canvas.restoreState()


# ─── 콘텐츠 생성 ────────────────────────────────────────────────────────────
def make_story(S):
    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # 표지
    # ══════════════════════════════════════════════════════════════════════════
    story += [sp(38)]
    story += [Paragraph('한글 팡팡 게임', S['cov_title']), sp(10)]
    story += [Paragraph('사용자 설명서', S['cov_sub']),    sp(28)]

    # 게임 정보 표
    cov_info = [
        ['내장 단어', '262개 (5단계)'],
        ['게임 시간', '60초'],
        ['최대 단어', '한 판 최대 20개'],
        ['단계 구성', '5단계 (한 글자 ~ 네 글자 + 종합)'],
        ['조작 방식', '터치 / 마우스 / 손동작(카메라)'],
        ['배포 주소', 'cjhong7.github.io/pangpang'],
    ]
    stats_data = [[Paragraph(safe(h), S['cov_th']) for h in ['구분', '내용']]]
    for k, v in cov_info:
        stats_data.append([Paragraph(safe(k), S['cov_th']),
                            Paragraph(safe(v), S['cov_td'])])
    stats_t = Table(stats_data, colWidths=[4*cm, COL_W - 4*cm])
    stats_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  colors.HexColor('#0d47a1')),
        ('BACKGROUND',    (0,1), (0,-1),  colors.HexColor('#1a3a6b')),
        ('BACKGROUND',    (1,1), (1,-1),  colors.HexColor('#1e2d5a')),
        ('ROWBACKGROUNDS',(1,1), (1,-1),  [colors.HexColor('#1e2d5a'),
                                           colors.HexColor('#182446')]),
        ('GRID',          (0,0), (-1,-1), 0.3, colors.HexColor('#2244aa')),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW',     (0,0), (-1,0),  1.0, colors.HexColor('#2255cc')),
    ]))
    story += [stats_t, sp(18)]

    # 목차 표
    toc_entries = [
        ['요약', '한 장 요약 (Quick Start) — 이 페이지만 읽어도 즉시 사용 가능'],
        ['1장', '게임 소개 및 특징'],
        ['2장', '실행 방법 (bat 파일 / GitHub Pages URL)'],
        ['3장', '화면 흐름 & 게임 플레이'],
        ['4장', '점수 체계 & 게임 규칙'],
        ['5장', '관리자 초기 설정'],
        ['6장', 'Google Sheets 연동 — GAS 설치 상세 안내'],
        ['7장', '엑셀로 단어 등록 (커스텀 단어)'],
        ['8장', '결과 분석 화면'],
        ['9장', '학년·반 관리 & 참여코드'],
        ['10장', '문제해결 & FAQ'],
    ]
    toc_data = [[Paragraph('목차', S['cov_toc_h']), Paragraph('내용', S['cov_toc_h'])]]
    for ch, title in toc_entries:
        toc_data.append([Paragraph(safe(ch),    S['cov_toc_ch']),
                         Paragraph(safe(title), S['cov_toc_t'])])
    toc_t = Table(toc_data, colWidths=[1.8*cm, COL_W - 1.8*cm])
    toc_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  colors.HexColor('#0d47a1')),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.HexColor('#131f4a'),
                                           colors.HexColor('#0f1a40')]),
        ('GRID',          (0,0), (-1,-1), 0.3, colors.HexColor('#2244aa')),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW',     (0,0), (-1,0),  1.0, colors.HexColor('#2255cc')),
    ]))
    story += [toc_t]

    # 본문 템플릿으로 전환
    story += [NextPageTemplate('body'), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 한 장 요약 (Quick Start)
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('한 장 요약 (Quick Start)  —  바쁘면 이 페이지만!', S), sp(8)]
    story += [info_box(
        '이 페이지만 읽어도 게임을 바로 운영할 수 있습니다. '
        '세부 내용은 각 장을 참조하세요.', S), sp(10)]

    story += [fmt('① 실행하기', S, 'qs_num')]
    story += [
        fmt('방법 A (로컬): 프로그램 폴더의 ' + b('게임실행하기.bat') + ' 파일을 더블클릭합니다.', S, 'qs_body'),
        fmt('방법 B (인터넷): 크롬 브라우저에서 ' + c('https://cjhong7.github.io/pangpang') + ' 접속합니다.', S, 'qs_body'),
        sp(6),
    ]

    story += [fmt('② 게임 방법', S, 'qs_num')]
    story += [
        fmt('1. 시작 화면에서 ' + b('오프라인') + '(기기 저장) 또는 ' + b('온라인') + '(클라우드 저장) 모드를 선택합니다.', S, 'qs_body'),
        fmt('2. 단계(1~5)를 선택하고 이름을 입력합니다 (음성 인식 또는 키보드).', S, 'qs_body'),
        fmt('3. 화면에 떠오르는 ' + b('비눗방울 중 정답 단어') + '를 터치 · 클릭 · 손동작으로 터뜨립니다.', S, 'qs_body'),
        fmt('4. 60초 안에 최대한 많이 맞혀 높은 점수를 받습니다.', S, 'qs_body'),
        fmt('5. 게임 종료 후 ' + b('오답이 있으면') + ' 틀린 단어 확인 화면이 뜹니다. ✋ 확인 후 다음 선택 화면으로 이동합니다.', S, 'qs_body'),
        sp(6),
    ]

    story += [fmt('③ 단계별 점수', S, 'qs_num')]
    qs_score = [
        ['1단계', '한 글자', '+2점', '예) 강, 산, 집'],
        ['2단계', '두 글자', '+4점', '예) 나무, 하늘'],
        ['3단계', '세 글자', '+6점', '예) 바나나, 토마토'],
        ['4단계', '네 글자', '+8점', '예) 사과나무'],
        ['5단계(종합)', '1~4단계 혼합', '+10점', '모든 단어 출제'],
    ]
    story += [make_table(S, ['단계', '대상', '정답', '예시'], qs_score,
                         col_widths=[2.5*cm, 2.8*cm, 1.8*cm, COL_W - 7.1*cm],
                         center_cols={0, 1, 2}), sp(4)]
    story += [note_box('오답(틀린 단어 선택) 시 -0.5점 감점됩니다.', S), sp(8)]

    story += [fmt('④ 조작 방법', S, 'qs_num')]
    qs_ctrl = [
        ['터치스크린', '손가락으로 비눗방울을 직접 터치'],
        ['마우스', '비눗방울 위에서 클릭'],
        ['손동작 (카메라)', '손바닥을 비눗방울 위에 0.5초 유지 → 자동 터뜨리기'],
    ]
    story += [make_table(S, ['조작', '방법'], qs_ctrl,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(8)]

    story += [fmt('⑤ 관리자 — 온라인 저장 연동 (선택)', S, 'qs_num')]
    story += [
        fmt('1. 시작 화면 우하단 [설정] → 학교명 + 비밀번호 입력(초기값: ' + b('0000') + ')', S, 'qs_body'),
        fmt('2. Google 스프레드시트 새 파일 → 확장 프로그램 → Apps Script', S, 'qs_body'),
        fmt('3. 환경설정 [' + b('GAS 코드 복사') + '] → Apps Script 에 붙여넣기(Ctrl+A → Delete → Ctrl+V) → 저장(Ctrl+S)', S, 'qs_body'),
        fmt('4. [배포] → [새 배포] → 웹 앱 → 액세스: 모든 사용자 → URL 복사 → 환경설정 [GAS URL] 에 붙여넣기 → 저장', S, 'qs_body'),
        sp(6),
    ]

    story += [fmt('⑥ 자주 묻는 문제 — 빠른 해결', S, 'qs_num')]
    qs_faq = [
        ['화면이 안 열려요', '크롬 브라우저에서 URL 직접 입력 또는 bat 파일 실행 (경로 한글/공백 금지)'],
        ['카메라 안 켜져요', 'HTTPS / localhost 환경 필요. 크롬 자물쇠 아이콘 → 카메라 허용'],
        ['비밀번호 잊었어요', 'F12 → Console → localStorage.removeItem("hpg_pw_admin_학교명") 실행'],
        ['점수 저장 안 돼요', '온라인 모드에서 GAS URL 설정 확인. 오프라인 모드는 기기에만 저장'],
        ['단어 바꾸고 싶어요', '엑셀(.xlsx)에 단어 작성 후 환경설정에서 업로드 (7장 참조)'],
    ]
    story += [make_table(S, ['증상', '빠른 해결'], qs_faq,
                         col_widths=[3.8*cm, COL_W - 3.8*cm]), sp(6)]
    story += [PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 1장: 게임 소개 및 특징
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('1장  게임 소개 및 특징', S), sp(10)]

    story += [fmt('1-1  게임 개요', S, 'h2')]
    story += [body(
        '한글 팡팡 게임은 초등학교 1~6학년 학생을 대상으로 하는 한글 단어 학습 웹게임입니다. '
        '교실 TV나 터치스크린에 크롬 브라우저 하나로 접속해 즉시 실행합니다. '
        '화면 위로 떠오르는 비눗방울 중에서 정답 단어를 찾아 터치하거나 손동작으로 터뜨리며 점수를 쌓습니다. '
        '별도 설치 없이 GitHub Pages URL로 학교 전체에서 동시 사용 가능합니다.', S), sp(6)]

    intro = [
        ['대상', '초등학교 1~6학년'],
        ['실행 환경', 'PC / 태블릿 / 터치스크린 + 크롬 브라우저'],
        ['게임 형태', '비눗방울 단어 찾기 — 60초 제한 시간'],
        ['내장 단어', '262개 (1글자~4글자 + 종합 5단계)'],
        ['조작 방식', '터치 / 마우스 / 카메라 손동작 (MediaPipe Hands)'],
        ['데이터 저장', '기기 저장(오프라인) 또는 구글 스프레드시트(온라인)'],
        ['배포 URL', 'https://cjhong7.github.io/pangpang'],
    ]
    story += [make_table(S, ['항목', '내용'], intro,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(10)]

    story += [fmt('1-2  주요 특징', S, 'h2')]
    features = [
        b('비눗방울 인터페이스') + ': 단어가 적힌 비눗방울이 카메라 실시간 배경 위에서 움직입니다. 교실 화면을 가득 채우는 화려한 비주얼로 학생의 집중을 끌어냅니다.',
        b('5단계 난이도') + ': 1글자(+2점) / 2글자(+4점) / 3글자(+6점) / 4글자(+8점) / 종합(+10점)으로 학년별 수준에 맞게 선택합니다.',
        b('손동작 인식 (MediaPipe Hands)') + ': 카메라에 손을 비추고 비눗방울 위에 0.5초 체류하면 자동으로 터집니다. 터치스크린이 없어도 게임 가능합니다.',
        b('음성 이름 입력 (Web Speech API)') + ': 게임 시작 시 이름을 음성으로 입력할 수 있습니다. 크롬 브라우저 HTTPS 환경에서 지원됩니다.',
        b('콤보 시스템') + ': 연속으로 정답을 맞히면 콤보 배율이 상승하여 점수가 빠르게 오릅니다.',
        b('QR 참여코드') + ': 학교전체 / 학년별 / 학년반별로 4자리 코드 및 QR 코드를 생성해 학생 기기에 배포합니다.',
        b('GAS 클라우드 연동') + ': Google Apps Script로 점수를 구글 스프레드시트에 자동 저장합니다. 학급·학년 단위 결과 분석이 가능합니다.',
        b('커스텀 단어 등록') + ': 엑셀(.xlsx) 파일로 단어를 업로드하면 내장 단어를 수업 주제에 맞게 교체할 수 있습니다.',
        b('배경음악(BGM)') + ': 환경설정에서 게임 중 배경음악 재생 여부를 설정합니다.',
    ]
    for f in features:
        story += [fmt('- ' + f, S, 'bullet'), sp(1)]
    story += [sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 2장: 실행 방법
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('2장  실행 방법', S), sp(10)]

    story += [fmt('2-1  방법 A: 로컬 실행 (bat 파일)', S, 'h2')]
    story += [body('인터넷 연결 없이 교실 PC에서 실행할 때 사용합니다.', S), sp(4)]
    run_files = [
        ['게임실행하기.bat', '크롬 브라우저로 게임 파일을 자동으로 엽니다 (더블클릭 1번)'],
        ['한글팡팡게임.html', '게임 본체 — bat 파일 없이 직접 열어도 됩니다'],
    ]
    story += [make_table(S, ['파일명', '역할'], run_files,
                         col_widths=[5.5*cm, COL_W - 5.5*cm], center_cols={0}), sp(8)]

    story += [fmt('실행 순서', S, 'h3')]
    for i, txt in enumerate([
        '게임 파일이 들어있는 폴더를 엽니다.',
        b('게임실행하기.bat') + ' 파일을 더블클릭합니다.',
        '크롬 브라우저가 자동으로 열리며 게임 시작 화면이 나타납니다.',
        '카메라를 사용하려면 브라우저 권한 요청에서 [허용]을 클릭합니다.',
    ], 1):
        story += [fmt('{}. '.format(i) + txt, S, 'num')]
    story += [sp(6)]
    story += [warn_box(
        '주의: 파일 경로에 한글 또는 공백이 포함되면 bat 파일이 오작동할 수 있습니다. '
        '이 경우 폴더를 C:\\pangpang 처럼 영문 경로로 이동하거나, '
        '방법 B(인터넷 접속)를 사용하세요.', S), sp(10)]

    story += [fmt('2-2  방법 B: 인터넷 브라우저 접속 (GitHub Pages)', S, 'h2')]
    story += [body('인터넷 연결 환경이라면 별도 설치 없이 URL 하나로 접속합니다. '
                   '음성 입력과 카메라 손동작 모두 정상 작동합니다.', S), sp(4)]
    story += [info_box(
        '접속 주소: https://cjhong7.github.io/pangpang\n'
        '크롬(Chrome) 브라우저 사용을 강력히 권장합니다.', S), sp(6)]

    browser_rows = [
        ['크롬 (Chrome)', '모든 기능 완전 지원 — 권장'],
        ['엣지 (Edge)', '대부분 지원. 음성 인식 일부 제한 가능'],
        ['파이어폭스 (Firefox)', '카메라·음성 제한. 권장하지 않음'],
        ['사파리 (Safari)', '모바일 일부 지원. 데스크탑은 제한 많음'],
    ]
    story += [make_table(S, ['브라우저', '지원 수준'], browser_rows,
                         col_widths=[4*cm, COL_W - 4*cm], center_cols={0}), sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 3장: 화면 흐름 & 게임 플레이
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('3장  화면 흐름 & 게임 플레이', S), sp(10)]

    story += [fmt('3-1  전체 화면 흐름', S, 'h2')]
    flow = [
        ['① 시작 화면', '오프라인 / 온라인 모드 선택', '오프라인: 기기 저장 / 온라인: 클라우드 저장'],
        ['② 단계 선택', '1~5단계 중 선택', '단계가 높을수록 긴 단어 + 높은 점수'],
        ['③ 이름 입력', '음성 또는 키보드로 이름 입력', '크롬 HTTPS 환경에서 음성 인식 자동 활성화'],
        ['④ 게임 화면', '비눗방울 터뜨리기 (60초)', '정답 단어를 찾아 터치 / 클릭 / 손동작'],
        ['⑤ 오답 확인', '틀린 단어 목록 표시 후 확인', '오답 0개이면 이 화면 생략'],
        ['⑥ 결과 화면', '점수, 정답률 표시 후 다음 선택', '다음 단계 / 새 플레이어 / 게임 종료 / 홈'],
    ]
    story += [make_table(S, ['화면', '주요 내용', '비고'], flow,
                         col_widths=[2.5*cm, 5.5*cm, COL_W - 8*cm]), sp(10)]

    story += [fmt('3-2  게임 화면 구성', S, 'h2')]
    story += [body(
        '게임이 시작되면 카메라 영상이 배경으로 깔리고 그 위에 비눗방울과 HUD가 표시됩니다. '
        '각 비눗방울에는 단어가 적혀 있으며 화면 안에서 랜덤으로 이동합니다.', S), sp(4)]
    hud = [
        ['상단 중앙', '남은 시간(초) + 현재 점수 실시간 표시'],
        ['상단 좌우', '현재 콤보 수, 정답/오답 횟수'],
        ['화면 전체', '단어가 적힌 비눗방울 (크기 다양, 랜덤 이동)'],
        ['화면 하단', '정답 단어 힌트 (단계별 설정에 따라 표시 여부 결정)'],
    ]
    story += [make_table(S, ['위치', '표시 내용'], hud,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(10)]

    story += [fmt('3-3  이름 입력 방법', S, 'h2')]
    name_rows = [
        ['음성 입력', '마이크 아이콘 자동 활성화 → 이름을 또렷하게 말하면 자동 입력', 'HTTPS + 크롬 브라우저 필요'],
        ['키보드 입력', '이름 입력칸에 직접 입력 후 [확인] 클릭 또는 Enter', '모든 환경 가능'],
    ]
    story += [make_table(S, ['방법', '절차', '조건'], name_rows,
                         col_widths=[2.5*cm, 8*cm, COL_W - 10.5*cm]), sp(10)]

    story += [fmt('3-4  손동작 (제스처) 조작', S, 'h2')]
    story += [body(
        '카메라가 연결된 환경에서 MediaPipe Hands 기반 손동작 인식이 자동으로 활성화됩니다. '
        '별도 설정 없이 카메라 권한만 허용하면 작동합니다.', S), sp(4)]
    gesture = [
        ['비눗방울 터뜨리기', '손바닥을 비눗방울 위치에 가져다 대기', '0.5초 체류 → 자동 터짐'],
        ['버튼 누르기', '손가락 끝을 버튼 위에 유지', '0.5초 체류 → 진행 게이지 후 실행'],
    ]
    story += [make_table(S, ['동작', '방법', '체류 시간'], gesture,
                         col_widths=[3.5*cm, 7.5*cm, COL_W - 11*cm], center_cols={0, 2}), sp(4)]
    story += [note_box(
        '팁: 배경이 밝고 손이 카메라에 잘 보이는 환경에서 인식률이 가장 높습니다. '
        '카메라와 손 사이 거리는 30~70cm가 적당합니다.', S), sp(10)]

    story += [fmt('3-5  오답 확인 화면', S, 'h2')]
    story += [body(
        '게임이 끝난 후 틀린 단어가 1개 이상 있으면 결과 화면으로 이동하기 전에 오답 확인 화면이 자동으로 표시됩니다. '
        '틀린 단어가 없으면 이 화면은 생략되고 바로 결과 화면으로 넘어갑니다.', S), sp(6)]
    wr_rows = [
        ['표시 조건', '게임 종료 시 오답(wrongWordsSession)이 1개 이상인 경우 자동 표시'],
        ['화면 내용', '틀린 단어를 카드 형태로 나열 + "N개의 단어를 틀렸어요" 안내 문구'],
        ['확인 버튼', '화면 하단 ✋ 확인 버튼 — 터치·마우스 클릭·손동작(0.5초 체류) 모두 가능'],
        ['다음 화면', '확인 버튼 선택 후 결과 화면으로 이동 (이어서 하기 / 새 참가자 / 종료 선택)'],
        ['딜레이', '확인 직후 2초간 손동작 감지 일시 정지 — 다음 화면 버튼 오작동 방지'],
    ]
    story += [make_table(S, ['항목', '설명'], wr_rows,
                         col_widths=[3*cm, COL_W - 3*cm]), sp(4)]
    story += [warn_box(
        '주의: 오답 확인 화면에서 ✋ 확인을 누른 직후 2초 동안은 손동작이 인식되지 않습니다. '
        '다음 화면의 버튼을 선택할 때 손이 이미 버튼 위에 있어도 2초 후부터 반응합니다.', S), sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 4장: 점수 체계 & 게임 규칙
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('4장  점수 체계 & 게임 규칙', S), sp(10)]

    story += [fmt('4-1  단계별 점수표', S, 'h2')]
    score = [
        ['1단계', '한 글자', '+2점', '-0.5점', '강, 산, 집, 불, 풀'],
        ['2단계', '두 글자', '+4점', '-0.5점', '나무, 하늘, 바람, 구름'],
        ['3단계', '세 글자', '+6점', '-0.5점', '바나나, 토마토, 사자자리'],
        ['4단계', '네 글자', '+8점', '-0.5점', '사과나무, 해바라기'],
        ['5단계 (종합)', '1~4단계 혼합', '+10점', '-0.5점', '모든 단어 랜덤 출제'],
    ]
    story += [make_table(S, ['단계', '대상', '정답', '오답', '예시 단어'], score,
                         col_widths=[2.8*cm, 2.8*cm, 1.8*cm, 1.8*cm, COL_W - 9.2*cm],
                         center_cols={0, 1, 2, 3}), sp(4)]
    story += [info_box(
        '점수는 소수점으로 누적됩니다. '
        '오답이 많으면 점수가 0점 이하로 내려갈 수 있습니다. '
        '콤보 시 점수 배율이 적용되어 높은 점수 달성이 가능합니다.', S), sp(10)]

    story += [fmt('4-2  게임 규칙', S, 'h2')]
    rules = [
        ['제한 시간', '60초. 시간이 끝나면 자동으로 결과 화면으로 이동'],
        ['최대 단어', '한 판에 비눗방울 최대 20개 출제'],
        ['출제 방식', '내장 262개 단어에서 랜덤 출제. 엑셀 업로드 시 해당 단어로 대체'],
        ['콤보 시스템', '연속 정답 시 콤보 증가, 연속 오답 시 콤보 초기화'],
        ['정답 선택', '현재 화면의 비눗방울 중 퀴즈 단어와 일치하는 단어를 선택'],
    ]
    story += [make_table(S, ['규칙', '설명'], rules,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(10)]

    story += [fmt('4-3  결과 화면 버튼', S, 'h2')]
    result_btns = [
        ['다음 단계로', '현재 플레이어 이름으로 한 단계 높여 즉시 재시작'],
        ['새로운 참여자', '이름 입력 화면으로 돌아가 새 플레이어 시작'],
        ['결과 분석', '현재까지 누적된 데이터 분석 화면 열기'],
        ['처음으로', '시작 화면(모드 선택)으로 이동'],
    ]
    story += [make_table(S, ['버튼', '동작'], result_btns,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 5장: 관리자 초기 설정
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('5장  관리자 초기 설정', S), sp(10)]

    story += [fmt('5-1  환경설정 열기', S, 'h2')]
    story += [fmt(
        '시작 화면 우하단의 ' + b('[설정]') + ' 아이콘(톱니바퀴)을 클릭합니다. '
        '학교명과 관리자 비밀번호를 입력하면 환경설정 패널이 열립니다. '
        '학교명은 참여코드 및 데이터 저장의 기준이 되므로 정확하게 입력합니다.', S), sp(4)]
    story += [imp_box(
        '초기 관리자 비밀번호: 0000  — 처음 설정 후 반드시 변경하세요!', S), sp(8)]

    story += [fmt('5-2  학교 정보 설정', S, 'h2')]
    school = [
        ['학교 이름', '학교명 정확히 입력. 변경 시 기존 데이터와 연결이 끊길 수 있음'],
        ['모드 선택', '오프라인(기기 저장만) 또는 온라인(GAS 클라우드 연동)'],
        ['GAS URL', '온라인 모드 사용 시 Google Apps Script 배포 URL 입력 (6장 참조)'],
    ]
    story += [make_table(S, ['항목', '설명'], school,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(10)]

    story += [fmt('5-3  관리자 비밀번호 변경', S, 'h2')]
    story += [body(
        '환경설정 하단 비밀번호 섹션에서 새 비밀번호를 입력하고 [변경] 버튼을 클릭합니다. '
        '비밀번호는 브라우저 localStorage에 학교명과 함께 저장됩니다.', S), sp(4)]
    story += [warn_box(
        '비밀번호 분실 시 복구 방법:\n'
        '크롬 F12 → Console 탭 → 아래 명령 실행 후 페이지 새로고침:\n'
        '  localStorage.removeItem("hpg_pw_admin_학교명")\n'
        '"학교명" 부분에 실제 설정한 학교 이름을 넣으세요.', S), sp(10)]

    story += [fmt('5-4  게임 설정 항목', S, 'h2')]
    game_set = [
        ['배경음악 (BGM)', '게임 중 배경음악 재생 여부 설정'],
        ['단어 업로드', '엑셀 파일로 커스텀 단어 등록 (7장 참조)'],
        ['학교전체 관리', '학교 단위 참여코드 생성 및 전체 데이터 초기화'],
        ['학년별 관리', '가(1학년) ~ 바(6학년) 선택 후 학년 코드 생성/초기화'],
        ['학년반별 관리', '학년 + 반 선택 후 반별 코드 생성/초기화'],
        ['GAS 코드 복사', 'GAS 설치에 사용할 스크립트 코드를 클립보드에 복사'],
    ]
    story += [make_table(S, ['항목', '기능'], game_set,
                         col_widths=[4*cm, COL_W - 4*cm], center_cols={0}), sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 6장: Google Sheets 연동 (GAS 설치)
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('6장  Google Sheets 연동 — GAS 설치 상세 안내', S), sp(10)]

    story += [fmt('6-1  연동 개요', S, 'h2')]
    story += [body(
        '온라인 모드에서는 게임 점수가 구글 스프레드시트에 자동 저장됩니다. '
        'Google Apps Script(GAS) 웹 앱이 중계 역할을 하며, '
        '설치는 7단계로 완료됩니다. '
        '연동 후에는 학급·학년·학교 단위 결과를 실시간으로 확인할 수 있습니다.', S), sp(4)]
    story += [info_box(
        '준비물: Google 계정 1개, 크롬 브라우저, 게임 환경설정 접근 가능한 상태', S), sp(8)]

    story += [fmt('6-2  단계별 설치 방법 (7단계)', S, 'h2')]

    gas_steps = [
        ('① 환경설정 열기',
         '시작 화면 [설정] 아이콘 클릭 → 학교명 + 관리자 비밀번호 입력'),
        ('② GAS 코드 복사',
         '환경설정 하단 [GAS 코드 복사] 버튼 클릭 → 코드가 클립보드에 복사됨'),
        ('③ 스프레드시트 생성',
         'Google Drive(drive.google.com) → [새로 만들기] → [Google 스프레드시트] 클릭'),
        ('④ Apps Script 열기',
         '스프레드시트 상단 메뉴 → [확장 프로그램] → [Apps Script] 클릭'),
        ('⑤ 코드 붙여넣기',
         'Apps Script 편집기에서 기존 코드 전체 선택(Ctrl+A) → 삭제(Delete) → '
         '붙여넣기(Ctrl+V) → 저장(Ctrl+S)'),
        ('⑥ 배포 실행',
         '오른쪽 상단 [배포] → [새 배포] → 유형: 웹 앱 → '
         '"다음 사용자로 실행: 나(자신)" → '
         '"액세스 권한: 모든 사용자(익명 포함)" → [배포] → URL 복사'),
        ('⑦ URL 입력 및 저장',
         '게임 환경설정 [GAS URL] 입력란에 복사한 URL 붙여넣기 → [저장] → '
         '[연결 테스트] 버튼으로 정상 연결 확인'),
    ]
    for label, detail in gas_steps:
        story += [KeepTogether([
            fmt(b(label), S, 'h3'),
            body(detail, S),
            sp(4),
        ])]
    story += [sp(2)]
    story += [warn_box(
        '중요: ⑥ 배포 시 액세스 권한을 반드시 "모든 사용자(익명 포함)"로 설정해야 합니다. '
        '"나만" 또는 "조직 내"로 설정하면 학생 기기에서 점수 저장이 되지 않습니다.', S), sp(8)]

    story += [fmt('6-3  저장 위치 (구글 시트 탭)', S, 'h2')]
    sheet_rows = [
        ['전체점수', '모든 게임 결과 — 학교명, 학년, 반, 이름, 점수, 단계, 날짜'],
        ['학년점수', '학년별 집계 요약 데이터'],
    ]
    story += [make_table(S, ['시트(탭) 이름', '저장 내용'], sheet_rows,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(8)]

    story += [fmt('6-4  저장 상태 메시지', S, 'h2')]
    msg_rows = [
        ['☁️ 저장 완료', '클라우드(구글 시트) 저장 성공'],
        ['✅ 기기 저장', '오프라인 모드 저장 성공'],
        ['❌ 연결 실패', 'GAS URL 오류 또는 네트워크 문제 → GAS URL 재확인 후 재배포'],
        ['⏳ 저장 중...', '데이터 전송 중 — 잠시 대기 (보통 1~3초)'],
    ]
    story += [make_table(S, ['메시지', '의미 및 조치'], msg_rows,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 7장: 엑셀로 단어 등록
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('7장  엑셀로 단어 등록 (커스텀 단어)', S), sp(10)]

    story += [fmt('7-1  개요', S, 'h2')]
    story += [body(
        '환경설정에서 엑셀(.xlsx) 파일을 업로드하면 내장 262개 단어 대신 '
        '업로드한 단어로 게임이 진행됩니다. '
        '수업 주제(과학 용어, 사회 단어, 영어 등)에 맞는 맞춤 단어를 사용할 수 있습니다.', S), sp(6)]

    story += [fmt('7-2  엑셀 파일 형식', S, 'h2')]
    story += [body('엑셀 첫 번째 행(헤더)에 단계명을 입력하고, 2행부터 단어를 세로로 입력합니다.', S), sp(4)]
    excel_tbl = [
        ['행', 'A열 (1단계)', 'B열 (2단계)', 'C열 (3단계)', 'D열 (4단계)', 'E열 (5단계)'],
        ['1행 (헤더)', '1단계', '2단계', '3단계', '4단계', '5단계'],
        ['2행~', '강', '나무', '바나나', '사과나무', '해바라기'],
        ['3행~', '산', '하늘', '토마토', '개나리꽃', '...'],
    ]
    tbl_hdr = excel_tbl[0]
    tbl_rows = excel_tbl[1:]
    story += [make_table(S, tbl_hdr, tbl_rows,
                         col_widths=[2.2*cm, 2.2*cm, 2.2*cm, 2.4*cm, 2.4*cm, COL_W - 11.4*cm],
                         center_cols={0, 1, 2, 3, 4, 5}), sp(6)]

    story += [fmt('7-3  작성 규칙', S, 'h3')]
    rules7 = [
        '파일 형식: .xlsx (Excel 2007 이상)',
        '헤더(1행): 반드시 "1단계" / "2단계" / "3단계" / "4단계" / "5단계" 로 입력',
        '단어는 각 열에 2행부터 세로로 입력 (한 행 = 한 단어)',
        '특정 단계를 비워두면 해당 단계는 내장 단어를 사용',
        '특수문자, 띄어쓰기 포함 단어도 입력 가능',
    ]
    for r in rules7:
        story += [bul(r, S)]
    story += [sp(8)]

    story += [fmt('7-4  업로드 방법', S, 'h2')]
    for i, txt in enumerate([
        '환경설정 → [단어 업로드] 버튼 클릭',
        '파일 선택 창에서 작성한 .xlsx 파일 선택',
        '파싱 완료 메시지 확인 (각 단계별 단어 수 표시)',
        '게임을 새로 시작하면 업로드한 단어로 진행됨',
    ], 1):
        story += [nm(i, txt, S)]
    story += [sp(4)]
    story += [info_box(
        '업로드한 단어는 브라우저 새로고침 후에도 유지됩니다 (localStorage 저장). '
        '원래 내장 단어로 돌아가려면 [단어 초기화] 버튼을 클릭하세요.', S), sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 8장: 결과 분석 화면
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('8장  결과 분석 화면', S), sp(10)]

    story += [fmt('8-1  결과 분석 열기', S, 'h2')]
    story += [body(
        '게임 결과 화면에서 [📊 결과분석] 버튼을 클릭합니다. '
        '또는 환경설정의 [학교전체 관리] / [학년별 관리] / [학년반별 관리] 섹션에서 '
        '[📊 결과분석] 버튼을 클릭해 해당 범위의 데이터를 분석합니다.', S), sp(6)]

    story += [fmt('8-2  분석 항목', S, 'h2')]
    analysis = [
        ['참여자 수', '분석 범위 내 총 플레이 횟수'],
        ['평균 점수', '전체 참여자의 평균 점수'],
        ['최고 점수', '1위 플레이어 이름 및 점수'],
        ['단계별 참여', '각 단계(1~5)별 참여 비율 및 평균 점수'],
        ['개인별 기록', '이름 / 단계 / 점수 / 게임 일시 목록'],
    ]
    story += [make_table(S, ['항목', '설명'], analysis,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(10)]

    story += [fmt('8-3  온라인 모드 — 클라우드 데이터 열람', S, 'h2')]
    story += [body(
        '온라인 모드에서는 구글 스프레드시트에서 데이터를 불러와 '
        '학교 전체 / 학년 / 반 단위로 비교 분석합니다. '
        '참여코드로 접속한 모든 기기의 데이터가 통합 집계됩니다.', S), sp(4)]
    cloud = [
        ['학교이름', '참여 학교명'],
        ['학년', '참여 학년 번호 (1~6)'],
        ['반', '참여 반 번호'],
        ['이름', '플레이어 이름'],
        ['점수', '최종 점수 (소수점 포함)'],
        ['단계', '플레이한 단계 (1~5)'],
        ['일시', '게임 완료 날짜 및 시각'],
    ]
    story += [make_table(S, ['열(Column)', '저장 내용'], cloud,
                         col_widths=[3.5*cm, COL_W - 3.5*cm], center_cols={0}), sp(10)]

    story += [fmt('8-4  엑셀 다운로드', S, 'h2')]
    story += [body(
        '결과 분석 화면에서 [엑셀 다운로드] 버튼을 클릭하면 '
        '현재 표시된 데이터를 .xlsx 파일로 내려받습니다. '
        '오프라인(기기) 데이터와 온라인(클라우드) 데이터를 각각 다운로드할 수 있습니다.', S), sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 9장: 학년·반 관리 & 참여코드
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('9장  학년·반 관리 & 참여코드', S), sp(10)]

    story += [fmt('9-1  참여코드 개요', S, 'h2')]
    story += [body(
        '참여코드는 학생이 게임 시작 시 소속(학교·학년·반)을 자동으로 설정하게 해주는 4자리 코드입니다. '
        '교사가 코드를 발급하고 학생에게 알려주면, 학생이 "학교이름"란에 코드를 입력해 '
        '소속 정보가 즉시 설정됩니다. QR 코드로도 배포 가능합니다.', S), sp(4)]
    codes = [
        ['학교전체 코드', '학교 단위', '학교 전체 집계, 새 학기 참여'],
        ['학년 코드', '특정 학년 (1~6학년)', '학년별 분석, 가~바 버튼 선택'],
        ['반 코드', '특정 학년 + 반', '반별 분석, 학년·반 순서로 선택'],
    ]
    story += [make_table(S, ['코드 종류', '적용 범위', '주요 용도'], codes,
                         col_widths=[3.5*cm, 4*cm, COL_W - 7.5*cm], center_cols={0, 1}), sp(10)]

    story += [fmt('9-2  학교전체 코드 발급', S, 'h2')]
    for i, txt in enumerate([
        '환경설정 → [학교전체 관리] 섹션으로 이동',
        '[🔗 참여코드 생성] 클릭 → 4자리 코드 발급',
        '[복사] 버튼으로 코드를 클립보드에 복사',
        '[QR] 버튼으로 QR 코드 이미지 표시 → 학생 스마트폰으로 스캔',
    ], 1):
        story += [nm(i, txt, S)]
    story += [sp(8)]

    story += [fmt('9-3  학년별 코드 발급', S, 'h2')]
    story += [fmt(
        '환경설정 → [학년별 관리]에서 ' + b('가(1학년) ~ 바(6학년)') +
        ' 버튼으로 학년을 선택한 뒤 [참여코드 생성] 클릭합니다. '
        '선택한 학년의 코드가 생성되며, 복사 및 QR 기능을 동일하게 사용합니다.', S), sp(8)]

    story += [fmt('9-4  학년반별 코드 발급', S, 'h2')]
    story += [body(
        '환경설정 → [학년반별 관리]에서 학년을 선택한 뒤 반 버튼(1반, 2반, 3반...)을 선택합니다. '
        '[🔗 참여코드 생성] 클릭 시 해당 학년·반 코드가 생성됩니다.', S), sp(8)]

    story += [fmt('9-5  코드 재발급 시 주의사항', S, 'h2')]
    story += [note_box(
        '참여코드를 재생성하면 이전 코드는 즉시 무효화됩니다. '
        '이미 이전 코드로 접속한 학생들에게 새 코드를 다시 안내해야 합니다.', S), sp(8)]

    story += [fmt('9-6  데이터 초기화', S, 'h2')]
    story += [imp_box(
        '경고: 데이터 초기화를 실행하면 해당 범위의 모든 오프라인 게임 기록이 영구 삭제됩니다. '
        '반드시 [엑셀 다운로드]로 백업한 후 초기화하세요. 이 작업은 되돌릴 수 없습니다.', S), sp(6)]
    init_rows = [
        ['학교전체 초기화', '학교 전체 기기 저장 데이터 삭제', '새 학기 시작 시'],
        ['학년별 초기화', '선택한 학년 기기 저장 데이터 삭제', '학년 교체 시'],
        ['반별 초기화', '선택한 학년·반 기기 저장 데이터 삭제', '학기 중 재시작 시'],
    ]
    story += [make_table(S, ['초기화 범위', '삭제 대상', '권장 시점'], init_rows,
                         col_widths=[4*cm, 5.5*cm, COL_W - 9.5*cm],
                         center_cols={0, 2}), sp(6), PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # 10장: 문제해결 & FAQ
    # ══════════════════════════════════════════════════════════════════════════
    story += [ch_hdr('10장  문제해결 & FAQ', S), sp(10)]

    faqs = [
        ('Q1. 게임 화면이 열리지 않아요.',
         '크롬 브라우저에서 URL(cjhong7.github.io/pangpang)을 직접 입력하거나 '
         'bat 파일을 실행하세요. bat 파일은 경로에 한글·공백이 없어야 합니다. '
         '없다면 폴더를 영문 경로(예: C:\\pangpang)로 이동 후 재시도합니다.'),
        ('Q2. 카메라가 켜지지 않아요.',
         '크롬 주소창 왼쪽 자물쇠 아이콘 → [사이트 설정] → 카메라 "허용"으로 변경 후 새로고침합니다. '
         'file:// 로컬 파일 방식에서는 카메라 미지원입니다. GitHub Pages URL로 접속하세요.'),
        ('Q3. 음성 이름 입력이 안 돼요.',
         '크롬 브라우저 + HTTPS 주소(github.io) 접속 환경에서만 지원됩니다. '
         '로컬 파일 방식에서는 사용 불가입니다. '
         '마이크 권한이 허용되어 있는지 브라우저 설정에서 확인하세요.'),
        ('Q4. 관리자 비밀번호를 잊었어요.',
         '크롬 F12 → Console 탭에 아래 명령을 입력 후 Enter:\n'
         '  localStorage.removeItem("hpg_pw_admin_학교명")\n'
         '"학교명" 부분에 설정한 실제 학교 이름을 넣습니다. '
         '새로고침 후 비밀번호 없이 설정 가능합니다.'),
        ('Q5. 구글 드라이브 연결 실패 메시지가 떠요.',
         'GAS URL이 올바른지 확인합니다. GAS 편집기 → [배포 관리] → 현재 배포 URL 복사 → '
         '환경설정에 다시 붙여넣기합니다. '
         '구글 서버 일시 장애일 수도 있으니 수 분 후 재시도하세요.'),
        ('Q6. 점수가 저장되지 않아요.',
         '오프라인 모드에서는 브라우저 localStorage에 저장됩니다. '
         '온라인 모드에서는 GAS URL 설정이 완료되어야 합니다. '
         '시크릿(개인정보 보호) 모드에서는 저장이 제한될 수 있습니다.'),
        ('Q7. 단어를 수업 주제에 맞게 바꾸고 싶어요.',
         '7장을 참조하세요. 엑셀(.xlsx) 파일에 단계별 단어를 작성해 '
         '환경설정에서 업로드하면 즉시 반영됩니다. '
         '원래 단어로 돌아가려면 [단어 초기화]를 누르세요.'),
        ('Q8. 학생이 참여코드를 잃어버렸어요.',
         '환경설정 → 해당 범위(학교전체·학년·반) 관리에서 기존 코드를 다시 확인하거나, '
         '[🔗 참여코드 생성]을 다시 눌러 재발급합니다. '
         '재발급 시 이전 코드는 무효화됩니다.'),
        ('Q9. 게임이 느리거나 끊겨요.',
         '다른 탭·앱을 닫고 크롬 브라우저만 실행하세요. '
         '카메라 해상도가 높으면 손동작 처리가 느릴 수 있습니다. '
         '카메라를 끄고 터치·마우스로만 사용해도 게임에 지장 없습니다.'),
        ('Q10. 스마트폰·태블릿에서도 사용 가능한가요?',
         '크롬 모바일 브라우저에서 접속 가능합니다. 터치 조작은 완전 지원됩니다. '
         '카메라 손동작 기능은 PC 환경에서 최적화되어 있으며, '
         '모바일에서는 터치 방식을 사용하는 것을 권장합니다.'),
    ]

    for q, a in faqs:
        story += [KeepTogether([
            fmt(b(q), S, 'h3'),
            body(a, S),
            sp(5),
        ])]

    story += [sp(10), hr(), sp(6)]
    story += [note_box(
        '추가 문의 및 버그 신고: github.com/cjhong7/pangpang/issues\n'
        '이 설명서는 2026년 6월 기준 한글 팡팡 게임 v2026.06에 맞게 작성되었습니다.', S)]

    return story


# ─── 1차 검토 ───────────────────────────────────────────────────────────────
# 검토 1: 내용 완전성
#   - Quick Start(한 장 요약): 실행·게임·점수·조작·GAS·FAQ 6항목 포함 ✓
#   - 1장: 개요표·주요특징 9가지 ✓
#   - 2장: bat/URL 양방법, 브라우저 지원표 ✓
#   - 3장: 화면흐름·HUD·이름입력·손동작 ✓
#   - 4장: 점수표·규칙·결과버튼 ✓
#   - 5장: 설정열기·학교정보·비밀번호·게임설정 ✓
#   - 6장: 7단계 GAS 설치·시트위치·상태메시지 ✓
#   - 7장: 파일형식·작성규칙·업로드 ✓
#   - 8장: 분석항목·클라우드·다운로드 ✓
#   - 9장: 코드종류·학교전체·학년·반별·재발급·초기화 ✓
#   - 10장: Q1~Q10 ✓
#
# 검토 2: 정확성
#   - 점수: +2/+4/+6/+8/+10, 오답 -0.5 ✓
#   - 게임시간: 60초, 최대단어: 20개 ✓
#   - 단계: 1글자·2글자·3글자·4글자·종합 5단계 ✓
#   - 초기 비밀번호: 0000 ✓
#   - localStorage 접두사: hpg_ ✓
#   - 배포 URL: cjhong7.github.io/pangpang ✓
#   - 내장단어: 262개 ✓
#   - 손동작 체류시간: 0.5초 ✓
#   - GAS 코드복사 버튼, GAS URL 입력란 ✓


def main():
    out = (r'C:\Users\user\Desktop\2026 연구학교 관련'
           r'\warp-project\pangpang\한글팡팡게임_사용자설명서.pdf')

    S = build_styles()

    cover_frame = Frame(1*cm, 2.5*cm, W - 2*cm, H - 6*cm, id='cover')
    body_frame  = Frame(2*cm, 2.5*cm, W - 4*cm, H - 4.8*cm, id='body')

    cover_tmpl = PageTemplate(id='cover', frames=[cover_frame], onPage=draw_cover)
    body_tmpl  = PageTemplate(id='body',  frames=[body_frame],  onPage=draw_body)

    doc = BaseDocTemplate(
        out,
        pagesize=A4,
        pageTemplates=[cover_tmpl, body_tmpl],
        title='한글 팡팡 게임 사용자 설명서',
        author='cjhong7',
    )

    story = make_story(S)
    doc.build(story)

    size_kb = os.path.getsize(out) // 1024
    print('생성 완료: ' + out)
    print('파일 크기: {} KB'.format(size_kb))


if __name__ == '__main__':
    main()
