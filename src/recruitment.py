"""Hiring terms from the salon's five published role descriptions."""
GROUPS = (
    ('新卒採用', 'New graduates', 'shinsotusaiyou.jpg', '美容学校からサロンへ。接客と施術の基礎を、営業中のレッスンで身につけます。', ('newgraduate',)),
    ('中途採用', 'Experienced hires', 'tyuuto2.jpg', '施術に集中したい方から、後輩の指導や店舗運営に挑戦したい方まで。経験に合う職種をお選びください。', ('midcareer_stylist', 'midcareer_assistant', 'midcareer_manager')),
    ('パート採用', 'Part-time', 'part2.jpg', '働ける曜日と時間を相談しながら、美容師としての経験を活かせます。', ('assistant',)),
)

BENEFITS = (
    ('健康と暮らし', '健康診断、予防接種の費用補助、引っ越し費用の補助、結婚・出産時のお祝い金があります。'),
    ('学びと資格', '外部セミナーや研修への参加費、資格に挑戦する際の受験費用を補助します。'),
    ('スタッフ特典', '社員割引のほか、紹介した方が採用された場合の報奨金は10万円です（会社規定による）。'),
)
HOURS = '10:00〜20:00の時間帯で所定8時間。週5〜6日、希望シフト制。'
DAYS_OFF = '週休2日制（月8〜9日休み）、年間休日110日。有給休暇は年10日。'
LEAVE = '年末年始（12月31日〜1月3日）、産前産後・育児・慶弔休暇、年3日のリフレッシュ休暇。'
LICENSE = '美容師免許（取得見込みを含む）。'
ALLOWANCES = '役職手当5,000〜50,000円、職務手当1,000〜50,000円、資格手当1,000〜20,000円。'
PAY_MID = '賞与の前年度実績は年2回・3万〜15万円。昇給あり。'
SHARED_TRAINING = '社内で1日、接客・接遇とサロンの仕事の進め方を学びます。'
MID_ALLOWANCES = ALLOWANCES + ' 住宅手当は月10,000円まで、皆勤手当は月5,000円まで。'
INSURANCE = '社会保険完備。'
ROLES = {
    'newgraduate': dict(
        lead='美容学校で学んだことを、お客様に向き合う技術へ。接客、シャンプー、施術の補助からサロンワークを身につけます。',
        detail='シャンプー、施術に使う道具の準備、お客様のお迎えから始めます。スタイリストの補助を通して、施術の流れと接客を身につけます。',
        name='新卒アシスタント', group='新卒採用', contract='正社員', pay='月給19万〜20万円',
        pay_basis='諸手当別・月払い', allowance='通勤手当。'+MID_ALLOWANCES,
        bonus='賞与の前年度実績は年2回・2万〜5万円。昇給率の掲載実績は10％。',
        hours=HOURS, overtime='なし', days=DAYS_OFF, leave=LEAVE, insurance=INSURANCE,
        qualification=LICENSE+' 未経験可。1〜4年制の専門学校を対象とし、既卒・第二新卒は卒業後3年以内まで応募できます。',
        training=SHARED_TRAINING+' 予約の合間にウィッグを使い、営業中にも技術を練習できます。'),
    'midcareer_stylist': dict(
        lead='カウンセリングから仕上げまで、一人のお客様に寄り添う仕事です。得意な技術を活かしながら提案の幅を広げられます。',
        detail='カット・カラー・パーマに加え、ご自宅でのお手入れをお伝えします。後輩のサポートや発信にもチームで携わります。',
        name='スタイリスト', group='中途採用', contract='正社員', pay='月給20万〜25万円',
        pay_basis='一律支給手当込み・月払い', board_pay='月給21.8万〜28.7万円＋歩合',
        allowance='通勤手当。'+MID_ALLOWANCES, bonus=PAY_MID,
        hours=HOURS, overtime='月平均10時間', days=DAYS_OFF,
        leave=LEAVE+' リフレッシュ休暇を含めて最大10連休の取得が可能です。', insurance=INSURANCE,
        qualification=LICENSE+' ジュニアスタイリスト以上の経験がある方。',
        training=SHARED_TRAINING+' 営業の合間には技術の見直し、後輩のレッスン、スタイルの写真撮影や発信も担当します。',
        example='入社1年で月間売上100万円・担当100名に達したスタッフの支給例は約30万円。月平均売上150万円のスタッフでは約35万〜45万円です。'),
    'midcareer_assistant': dict(
        lead='シャンプーやカラーの補助、お客様をお迎えする準備など。いま出来ることを確かめながら次の技術へ進みます。',
        detail='施術の準備、シャンプー、カラー補助などを担当。営業の合間のレッスンを通じて、サロンで使う手技を習得します。',
        name='中途アシスタント', group='中途採用', contract='正社員', pay='月給19万〜20万円',
        pay_basis='一律支給手当込み・月払い', board_pay='月給19.7万〜20.7万円＋歩合（週5日・1日8時間の掲載枠）',
        allowance='通勤手当は月10,000円まで。'+MID_ALLOWANCES, bonus=PAY_MID,
        hours=HOURS, overtime='月平均10時間', days=DAYS_OFF, leave=LEAVE, insurance=INSURANCE,
        qualification=LICENSE, training=SHARED_TRAINING+' 接客と施術の補助を担当しながら、営業時間内にシャンプーやカラーなどの練習を重ねます。'),
    'midcareer_manager': dict(
        lead='お客様を担当する美容師としての仕事と、スタッフの育成やサロン運営を担うポジションです。',
        detail='お客様への施術を中心に、アシスタントの技術指導やチームの連携、店舗づくりに携わります。',
        name='店長', group='中途採用', contract='正社員', pay='月給30万円',
        pay_basis='一律支給手当込み・月払い', allowance='通勤手当。'+MID_ALLOWANCES,
        bonus='賞与の前年度実績は年2回・3万〜15万円。昇給額の掲載実績は1,000〜5,000円。',
        hours='10:00〜20:00の時間帯で所定8時間。月20〜22日、希望シフト制。10:00〜18:00、12:00〜20:00などの勤務例があります。',
        overtime='月平均10時間', days=DAYS_OFF, leave=LEAVE, insurance=INSURANCE,
        qualification=LICENSE+' スタイリスト以上の経験がある方。',
        training=SHARED_TRAINING+' ミルボンに委託した3日間の店長研修と、月1回の社長面談があります。'),
    'assistant': dict(
        lead='家庭の予定と両立しながら、お客様のカット・カラー・仕上げまでを担当します。',
        detail='希望する曜日や時間帯に合わせて、カウンセリング、カット、カラー、仕上げを担当します。',
        name='パートスタイリスト', group='パート採用', contract='パート・アルバイト', pay='時給1,500円',
        pay_basis='スタイリストの時給・諸手当別・月払い', allowance='通勤手当、皆勤手当（実費）。'+ALLOWANCES,
        bonus='賞与の掲載実績は年2回・2万〜5万円。昇給率の掲載実績は10％。',
        hours='10:00〜20:00の間で1日3〜8時間、週2〜6日。勤務時間と休日は希望シフト制です。',
        overtime='なし', days='勤務日数・曜日に合わせて相談できます。', leave='お子さまの急な体調変化やけがの際はご相談ください。',
        insurance='健康保険・厚生年金・雇用保険・労災保険は、勤務条件に応じて適用されます。',
        qualification=LICENSE+' ジュニアスタイリスト以上の経験がある方。アシスタントでのパート勤務を希望する方は、担当業務と募集状況を採用担当にご確認ください。',
        training=SHARED_TRAINING, example='正社員登用制度があります。サロン公表時点で、過去3年間に3名がパートから正社員になりました。'),
}
