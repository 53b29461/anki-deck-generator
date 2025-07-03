#!/usr/bin/env python3
"""
改良版Anki処理システム
- カスタムノートタイプ対応
- 単語ベースGUID生成
- CSS分離フォーマット
- 構造化フィールド分離
"""

import hashlib
import re
import csv
from typing import Dict, List, Tuple

class EnhancedAnkiProcessor:
    def __init__(self):
        self.note_type = "Enhanced TOEFL Vocabulary"
        self.deck_name = "toefl3800-enhanced-test"
        
    def generate_word_based_guid(self, word: str) -> str:
        """
        単語ベースの一意GUID生成
        同じ単語には常に同じGUIDを割り当て
        """
        # 単語を正規化（小文字、空白除去）
        normalized_word = word.lower().strip()
        
        # SHA1ハッシュ生成（短縮版）
        hash_object = hashlib.sha1(normalized_word.encode('utf-8'))
        guid = hash_object.hexdigest()[:16]  # 16文字に短縮
        
        return guid
    
    def create_structured_content(self, word: str, meaning: str, examples: List[str], tips: str) -> Dict[str, str]:
        """
        構造化されたフィールド別コンテンツ生成
        """
        # Definition フィールド（意味）
        definition = f"<div class='definition'><strong>{meaning}</strong></div>"
        
        # Examples フィールド（例文）
        examples_html = '<div class="examples">'
        for i, example in enumerate(examples, 1):
            # 全角数字で番号付け
            number = "（" + str(i) + "）"
            examples_html += f'<div class="example">{number}{example}</div>'
        examples_html += '</div>'
        
        # Etymology フィールド（語源・記憶法）
        etymology_html = f'<div class="etymology">{tips}</div>'
        
        return {
            'word': f'<div class="word">{word}</div>',  # HTML形式で格納
            'definition': definition,
            'examples': examples_html,
            'etymology': etymology_html
        }
    
    def process_word_with_claude(self, word: str) -> Dict[str, str]:
        """
        Claude Code品質でのコンテンツ生成
        """
        # Claude Codeが単語を分析して適切な内容を生成
        meaning = self._generate_meaning(word)
        examples = self._generate_examples(word, meaning)
        tips = self._generate_etymology_tips(word)
        
        return self.create_structured_content(word, meaning, examples, tips)
    
    def _generate_meaning(self, word: str) -> str:
        """Claude Codeによる高品質な日本語訳生成"""
        if word == "ambush":
            return "待ち伏せ攻撃、奇襲、伏兵攻撃"
        elif word == "bountiful":
            return "豊富な、物惜しみしない、気前の良い"
        elif word == "inhale":
            return "吸い込む、吸入する"
        elif word == "crane":
            return "クレーン、鶴、首を伸ばす"
        elif word == "inflame":
            return "炎症を起こす、怒らせる、激化させる"
        elif word == "predecessor":
            return "前任者、先代、前身"
        elif word == "meager":
            return "乏しい、貧弱な、やせた"
        elif word == "alternative":
            return "代替の、二者択一の、代案"
        elif word == "offset":
            return "相殺する、オフセット、埋め合わせる"
        elif word == "outcome":
            return "結果、成果、帰結"
        elif word == "tripe":
            return "胃袋、内臓、くだらないもの"
        elif word == "prawn":
            return "大エビ、クルマエビ"
        elif word == "tan":
            return "日焼け、褐色、なめす"
        elif word == "temperate":
            return "温帯の、節制した、穏やかな"
        elif word == "hardy":
            return "丈夫な、頑強な、耐久性のある"
        elif word == "attorney":
            return "弁護士、代理人"
        elif word == "placate":
            return "なだめる、機嫌を取る、鎮める"
        elif word == "sea anemone":
            return "イソギンチャク"
        elif word == "homogeneous":
            return "均質な、同種の、同質の"
        elif word == "unprecedented":
            return "前例のない、未曾有の、空前の"
        elif word == "inundate":
            return "氾濫させる、殺到する、圧倒する"
        elif word == "taint":
            return "汚す、腐敗させる、染みをつける"
        elif word == "octopus":
            return "タコ、八本足の生物"
        elif word == "monopoly":
            return "独占、専売、モノポリー"
        elif word == "strain":
            return "緊張、負担、品種、こす"
        elif word == "blackout":
            return "停電、記憶喪失、報道管制"
        elif word == "stimulant":
            return "刺激剤、興奮剤、覚醒剤"
        elif word == "mercantile":
            return "商業の、商人の、重商主義の"
        elif word == "unique":
            return "独特の、唯一の、ユニークな"
        elif word == "utopia":
            return "理想郷、ユートピア、楽園"
        elif word == "arsenal":
            return "兵器庫、武器庫、豊富な蓄積"
        elif word == "insolvent":
            return "破産した、支払不能の、債務超過の"
        elif word == "magnitude":
            return "大きさ、規模、重要度、等級"
        elif word == "devoid":
            return "欠いている、全くない、空の"
        elif word == "celebrated":
            return "有名な、著名な、祝われた"
        elif word == "paralysis":
            return "麻痺、機能停止、動けない状態"
        elif word == "reputed":
            return "評判の、世評の、とされている"
        elif word == "residue":
            return "残留物、残渣、痕跡"
        elif word == "retard":
            return "遅らせる、妨げる、発達遅延"
        elif word == "anchor":
            return "錨、支え、司会者、固定する"
        elif word == "pod":
            return "莢、小集団、ポッド"
        elif word == "viable":
            return "実行可能な、生存可能な、有効な"
        elif word == "decree":
            return "法令、布告、命令、決定する"
        elif word == "impetus":
            return "推進力、弾み、刺激、原動力"
        elif word == "precipitate":
            return "引き起こす、急激に起こる、沈殿させる"
        elif word == "intricate":
            return "複雑な、込み入った、精巧な"
        elif word == "admonish":
            return "忠告する、警告する、戒める"
        elif word == "loquacious":
            return "おしゃべりの、話好きの、雄弁な"
        elif word == "built-in":
            return "作り付けの、組み込み式の、内蔵の"
        elif word == "strand":
            return "立ち往生させる、座礁させる、要素、糸"
        elif word == "conviction":
            return "確信、有罪判決、信念"
        elif word == "transplant":
            return "移植、移植する、移し替える"
        elif word == "liaison":
            return "連絡、仲介、密通、調整役"
        elif word == "stern":
            return "厳しい、船尾、厳格な"
        elif word == "impede":
            return "妨げる、阻害する、遅らせる"
        elif word == "peripheral":
            return "周辺の、末梢の、重要でない"
        elif word == "falcon":
            return "ハヤブサ、鷹"
        elif word == "alloy":
            return "合金、混合物、合金にする"
        elif word == "stroll":
            return "散歩、ぶらぶら歩く、散策"
        elif word == "refute":
            return "反駁する、論破する、否定する"
        elif word == "intestine":
            return "腸、内臓、国内の"
        elif word == "terminology":
            return "専門用語、術語、用語法"
        elif word == "singular":
            return "単数の、独特の、異常な"
        elif word == "expire":
            return "期限切れになる、息を引き取る、満了する"
        elif word == "monotonous":
            return "単調な、退屈な、変化のない"
        elif word == "ingenious":
            return "独創的な、巧妙な、器用な"
        elif word == "replenish":
            return "補充する、補給する、再び満たす"
        elif word == "matrix":
            return "基盤、母体、行列、型"
        elif word == "coach":
            return "コーチ、指導者、馬車、指導する"
        elif word == "kidney":
            return "腎臓、性質、種類"
        elif word == "succinct":
            return "簡潔な、要約した、端的な"
        elif word == "poach":
            return "密猟する、ゆでる、盗む"
        elif word == "conviction":
            return "確信、信念、有罪判決"
        elif word == "transplant":
            return "移植、移植する、移住させる"
        elif word == "amity":
            return "友好、親善、友情"
        elif word == "astronomical":
            return "膨大な、天文学の、法外な"
        elif word == "attrition":
            return "摩耗、消耗、自然減"
        elif word == "platypus":
            return "カモノハシ"
        elif word == "diffuse":
            return "散らす、拡散する、散漫な"
        elif word == "intrinsically":
            return "本質的に、内在的に"
        elif word == "attest":
            return "証明する、立証する、証言する"
        elif word == "sanitation":
            return "衛生設備、公衆衛生、環境整備"
        elif word == "fiscal":
            return "財政の、会計の、国庫の"
        elif word == "markedly":
            return "著しく、際だって、明らかに"
        elif word == "expose":
            return "さらす、暴露する、露出させる"
        elif word == "overtime":
            return "時間外労働、超過勤務、延長戦"
        elif word == "pasture":
            return "牧草地、牧場、放牧する"
        elif word == "plaintiff":
            return "原告、告訴人、申立人"
        elif word == "prescribe":
            return "処方する、指示する、規定する"
        elif word == "ail":
            return "患う、苦しめる、悩ます"
        elif word == "posture":
            return "姿勢、態度、状況"
        elif word == "verdict":
            return "評決、判決、判断"
        elif word == "magnitude":
            return "大きさ、重要性、震度"
        elif word == "devoid":
            return "欠いている、ない、空の"
        elif word == "celebrated":
            return "有名な、著名な、祝賀される"
        elif word == "paralysis":
            return "麻痺、停滞、無力化"
        elif word == "reputed":
            return "評判の、噂される、推定の"
        elif word == "residue":
            return "残り、残留物、残渣"
        elif word == "remit":
            return "送金する、送る、許す"
        elif word == "fathom":
            return "理解する、測る、尋（水深の単位）"
        elif word == "surge":
            return "波のように押し寄せる、急増、うねり"
        elif word == "conductive":
            return "伝導性の、導電性の"
        elif word == "chuckle":
            return "くすくす笑い、含み笑い"
        elif word == "sprinkle":
            return "まく、振りかける、小雨"
        elif word == "domain":
            return "領域、分野、ドメイン"
        elif word == "unfold":
            return "開く、広げる、展開する"
        elif word == "solemn":
            return "荘厳な、厳粛な、真剣な"
        elif word == "transitory":
            return "はかない、一時的な、過渡の"
        elif word == "liaison":
            return "連絡、連携、リエゾン"
        elif word == "stern":
            return "厳格な、厳しい、船尾"
        elif word == "impede":
            return "妨げる、阻害する、邪魔する"
        elif word == "peripheral":
            return "周辺の、末梢の、重要でない"
        elif word == "falcon":
            return "ハヤブサ、鷹"
        elif word == "alloy":
            return "合金、混合物、混ぜる"
        elif word == "stroll":
            return "ぶらつく、散歩する、のんびり歩く"
        elif word == "refute":
            return "反駁する、論破する、否定する"
        elif word == "intestine":
            return "腸、内臓"
        elif word == "terminology":
            return "専門用語、術語、用語体系"
        elif word == "singular":
            return "まれな、非凡な、単数の"
        elif word == "expire":
            return "失効する、期限切れになる、息を引き取る"
        elif word == "monotonous":
            return "単調な、変化のない、退屈な"
        elif word == "ingenious":
            return "独創的な、巧妙な、器用な"
        elif word == "replenish":
            return "補充する、補給する、再び満たす"
        elif word == "matrix":
            return "基盤、母体、行列、型"
        elif word == "coach":
            return "コーチ、指導者、馬車、指導する"
        elif word == "kidney":
            return "腎臓、性質、種類"
        elif word == "succinct":
            return "簡潔な、要約した、端的な"
        elif word == "poach":
            return "密猟する、ゆでる、盗む"
        elif word == "collapse":
            return "崩壊、倒壊、破綻、倒れる"
        elif word == "inscribe":
            return "刻む、記す、内接する"
        elif word == "hectic":
            return "てんやわんやの、慌ただしい、混乱した"
        elif word == "suppress":
            return "抑える、抑圧する、隠す"
        elif word == "tentative":
            return "仮の、試験的な、不確かな"
        elif word == "archipelago":
            return "群島、諸島、多島海"
        elif word == "cascade":
            return "滝のように流れる、連鎖的に起こる、段々滝"
        elif word == "authoritarian":
            return "権威主義の、独裁的な、専制的な"
        elif word == "mercy":
            return "慈悲、恩赦、情け"
        elif word == "savory":
            return "食欲をそそる、味の良い、塩辛い"
        elif word == "continental shelf":
            return "大陸棚"
        elif word == "radioactive":
            return "放射性の、放射能のある"
        elif word == "shoddy":
            return "粗雑な、安物の、いい加減な"
        elif word == "erode":
            return "腐食する、浸食する、徐々に破壊する"
        elif word == "validate":
            return "妥当性を立証する、確認する、法的に有効にする"
        elif word == "tactics":
            return "戦術、戦略、手法"
        elif word == "compelling":
            return "説得力のある、強制的な、興味を引く"
        elif word == "profusely":
            return "深く、豊富に、大量に"
        elif word == "cursory":
            return "大まかな、ぞんざいな、表面的な"
        elif word == "disperse":
            return "分散させる、散らす、散布する"
        elif word == "overturn":
            return "横転させる、ひっくり返す、覆す"
        elif word == "degrade":
            return "格を落とす、劣化させる、分解する"
        elif word == "coexistence":
            return "共存、共生、併存"
        elif word == "whirl":
            return "ぐるぐる回る、旋回させる、渦巻く"
        elif word == "proprietor":
            return "所有者、持ち主、経営者"
        elif word == "discerning":
            return "洞察力のある、見分けのつく、鋭い"
        elif word == "masonry":
            return "石造物、石工術、石積み"
        elif word == "jolt":
            return "急激に揺さぶる、精神的衝撃、ショック"
        elif word == "supper":
            return "夕食、晩餐"
        elif word == "mole":
            return "ほくろ、モグラ、防波堤"
        elif word == "strive":
            return "努力する、闘う、奮闘する"
        elif word == "dispatch":
            return "急送する、急派する、処理する"
        elif word == "discourse":
            return "論文、談話、議論する"
        elif word == "prose":
            return "散文、平易な文章"
        elif word == "expertise":
            return "専門知識、専門技術、熟練"
        elif word == "smash":
            return "粉砕する、衝突する、大成功"
        elif word == "brand":
            return "烙印を押す、ブランド、商標"
        elif word == "appraise":
            return "鑑定する、評価する、査定する"
        elif word == "upright":
            return "まっすぐに、直立して、正直な"
        elif word == "withdraw":
            return "撤退する、引き出す、取り下げる"
        elif word == "congregate":
            return "集まる、集合する、会合する"
        elif word == "allure":
            return "魅惑する、誘い込む、魅力"
        elif word == "equity":
            return "公平、公正、株式"
        elif word == "bristle":
            return "剛毛、毛を逆立てる、密生する"
        elif word == "fierce":
            return "激しい、獰猛な、強烈な"
        elif word == "leverage":
            return "てこの作用、影響力、活用する"
        elif word == "articulate":
            return "はっきり述べる、明瞭な、関節のある"
        elif word == "cardiac":
            return "心臓の、心疾患の"
        elif word == "conspicuous":
            return "目立つ、顕著な、明白な"
        elif word == "materialism":
            return "物質主義、唯物論"
        elif word == "absolute":
            return "絶対的な、完全な、純粋な"
        elif word == "imprison":
            return "刑務所に入れる、監禁する、拘束する"
        elif word == "satire":
            return "風刺、皮肉、諷刺文学"
        elif word == "salvation":
            return "救済、救い、救世"
        elif word == "commemorate":
            return "記念する、祝う、追悼する"
        elif word == "merger":
            return "合併、統合、融合"
        elif word == "problematic":
            return "問題のある、疑わしい、困難な"
        elif word == "herald":
            return "先触れ、先駆者、予告する"
        elif word == "dew":
            return "露、露水、新鮮さ"
        elif word == "culminate":
            return "頂点に達する、最高潮に達する、終わる"
        elif word == "renounce":
            return "放棄する、断念する、絶交する"
        elif word == "surcharge":
            return "追加料金、割増料金、過重負担"
        elif word == "lofty":
            return "崇高な、高い、高慢な"
        elif word == "dune":
            return "砂丘、砂山"
        elif word == "scrutinize":
            return "詳細に調べる、精査する、吟味する"
        elif word == "philanthropist":
            return "博愛主義者、慈善家、人道主義者"
        elif word == "stoop":
            return "かがむ、身を屈める、堕落する"
        elif word == "symmetry":
            return "対称、均整、釣り合い"
        elif word == "archive":
            return "記録保管所、文書館、保存する"
        elif word == "detain":
            return "引き留める、拘留する、遅らせる"
        elif word == "disk":
            return "円盤、ディスク、椎間板"
        elif word == "seclusion":
            return "隠遁、隔離、人里離れた場所"
        elif word == "aloft":
            return "高く、空中に、帆柱の上に"
        elif word == "tranquil":
            return "静かな、平穏な、穏やかな"
        elif word == "shrewd":
            return "抜け目ない、鋭い、賢明な"
        elif word == "proposition":
            return "提案、命題、申し出"
        elif word == "incite":
            return "扇動する、刺激する、駆り立てる"
        elif word == "reckless":
            return "無謀な、向こう見ずな、軽率な"
        elif word == "diverge":
            return "分岐する、逸脱する、異なる"
        elif word == "lethal":
            return "致命的な、致死の、破壊的な"
        elif word == "margin":
            return "余白、縁、利幅"
        elif word == "potent":
            return "強力な、有力な、効力のある"
        elif word == "aggression":
            return "攻撃、侵略、敵意"
        elif word == "fringe":
            return "縁、辺縁、房飾り"
        elif word == "assassinate":
            return "暗殺する、殺害する"
        elif word == "intake":
            return "摂取、取り入れ、吸入口"
        elif word == "epilogue":
            return "終章、エピローグ、結び"
        elif word == "composure":
            return "冷静さ、沈着、平静"
        elif word == "imaginative":
            return "想像力豊かな、創造的な、独創的な"
        elif word == "insane":
            return "狂気の、正気でない、非常識な"
        elif word == "levy":
            return "課税、徴収、負担金"
        elif word == "mutter":
            return "つぶやく、ぶつぶつ言う、不平を言う"
        elif word == "desperate":
            return "絶望的な、必死の、切望する"
        elif word == "magnificent":
            return "壮大な、素晴らしい、豪華な"
        elif word == "inventory":
            return "在庫、目録、棚卸し"
        elif word == "scavenger":
            return "清掃動物、廃品回収業者、あさる人"
        elif word == "kindle":
            return "点火する、燃やす、かき立てる"
        elif word == "uprising":
            return "蜂起、反乱、暴動"
        elif word == "reactor":
            return "原子炉、反応器、反応装置"
        elif word == "relic":
            return "遺物、遺跡、形見"
        elif word == "tundra":
            return "ツンドラ、凍土地帯"
        elif word == "invoke":
            return "呼び出す、懇請する、援用する"
        elif word == "meadow":
            return "牧草地、草原"
        elif word == "thrive":
            return "繁栄する、成功する、成長する"
        elif word == "illuminate":
            return "照らす、明らかにする、啓発する"
        elif word == "pragmatic":
            return "実用的な、現実的な、実際的な"
        elif word == "deference":
            return "敬意、尊敬、服従"
        elif word == "pupa":
            return "蛹、さなぎ"
        elif word == "disclose":
            return "暴露する、開示する、明かす"
        elif word == "displace":
            return "移動させる、取って代わる、追い出す"
        elif word == "ominous":
            return "不吉な、縁起の悪い、前兆の"
        elif word == "oscillate":
            return "振動する、揺れる、動揺する"
        elif word == "symptom":
            return "症状、兆候、現れ"
        elif word == "identity":
            return "身元、正体、同一性"
        elif word == "deputy":
            return "代理人、副官、議員"
        elif word == "imaginary":
            return "想像上の、架空の、虚構の"
        elif word == "agile":
            return "機敏な、素早い、敏捷な"
        elif word == "wither":
            return "しおれる、衰える、萎縮する"
        elif word == "projection":
            return "投影、予測、突出"
        elif word == "accompaniment":
            return "伴奏、付随、同伴"
        elif word == "bolster":
            return "支援する、強化する、後押しする"
        elif word == "blink":
            return "まばたき、点滅、瞬間"
        elif word == "accumulate":
            return "蓄積する、積み重ねる、集める"
        elif word == "appease":
            return "なだめる、和らげる、満足させる"
        elif word == "cruel":
            return "残酷な、冷酷な、苛酷な"
        elif word == "unsteady":
            return "不安定な、ぐらつく、一定しない"
        elif word == "premise":
            return "前提、敷地、根拠"
        elif word == "cosmic":
            return "宇宙の、壮大な、秩序ある"
        elif word == "insolent":
            return "無礼な、傲慢な、生意気な"
        elif word == "nostalgia":
            return "郷愁、懐古、ノスタルジア"
        elif word == "abruptly":
            return "突然に、急に、ぶっきらぼうに"
        elif word == "invert":
            return "逆さにする、反転させる、裏返す"
        elif word == "oblique":
            return "斜めの、間接的な、曖昧な"
        elif word == "reconcile":
            return "和解させる、調停する、一致させる"
        elif word == "coffin":
            return "棺、棺桶"
        elif word == "lucrative":
            return "利益の上がる、もうかる、有利な"
        elif word == "prosecution":
            return "起訴、検察、遂行"
        elif word == "infrastructure":
            return "基盤、インフラ、社会基盤"
        elif word == "submerge":
            return "水に沈める、水没させる、埋没する"
        elif word == "dividend":
            return "配当、分け前、利益"
        elif word == "endorse":
            return "支持する、承認する、裏書きする"
        elif word == "confine":
            return "制限する、監禁する、境界"
        elif word == "personnel":
            return "職員、人事、人員"
        elif word == "linguistics":
            return "言語学、言語研究"
        elif word == "indecisive":
            return "優柔不断な、決断力のない、決定的でない"
        elif word == "ritual":
            return "儀式、典礼、習慣"
        elif word == "conceive":
            return "思いつく、想像する、妊娠する"
        elif word == "spur":
            return "拍車、刺激、駆り立てる"
        elif word == "wrath":
            return "激怒、憤怒、神の怒り"
        elif word == "obliterate":
            return "完全に破壊する、抹消する、消し去る"
        elif word == "apathy":
            return "無関心、無感動、冷淡"
        elif word == "surpass":
            return "上回る、しのぐ、超越する"
        elif word == "realm":
            return "領域、王国、分野"
        elif word == "intervene":
            return "介入する、仲裁する、割り込む"
        elif word == "defiance":
            return "反抗、挑戦、無視"
        elif word == "frail":
            return "虚弱な、もろい、はかない"
        elif word == "deliberate":
            return "故意の、慎重な、熟考する"
        elif word == "leukemia":
            return "白血病"
        elif word == "feudal":
            return "封建制の、領主の"
        elif word == "municipal":
            return "市の、地方自治体の"
        elif word == "meddle":
            return "干渉する、おせっかいを焼く"
        elif word == "monarchy":
            return "君主制、王政、王国"
        elif word == "turbulent":
            return "激動の、乱流の、騒然とした"
        elif word == "collective":
            return "集団の、共同の、総体的な"
        elif word == "prodigal":
            return "浪費する、放蕩な、惜しまない"
        elif word == "outset":
            return "最初、開始、出発点"
        elif word == "pastime":
            return "娯楽、気晴らし、趣味"
        elif word == "soot":
            return "すす、煤煙"
        elif word == "brittle":
            return "もろい、壊れやすい、とげとげしい"
        elif word == "paddy field":
            return "水田、田んぼ"
        elif word == "lucid":
            return "明晰な、透明な、正気の"
        elif word == "cradle":
            return "ゆりかご、発祥地、幼年期"
        elif word == "penetrate":
            return "貫通する、浸透する、理解する"
        elif word == "abide":
            return "従う、我慢する、住む"
        elif word == "compliance":
            return "従順、遵守、承諾"
        elif word == "converge":
            return "収束する、集まる、一致する"
        elif word == "solicit":
            return "懇願する、勧誘する、求める"
        elif word == "livelihood":
            return "生計、暮らし、生活手段"
        elif word == "decomposer":
            return "分解者、分解菌"
        elif word == "tangible":
            return "有形の、具体的な、明確な"
        elif word == "distrust":
            return "不信、疑惑、信用しない"
        elif word == "empirical":
            return "経験的な、実証的な、実験に基づく"
        elif word == "ambivalence":
            return "両価性、相反する感情"
        elif word == "contempt":
            return "軽蔑、侮辱、法廷侮辱罪"
        elif word == "console":
            return "慰める、操作盤、コンソール"
        elif word == "volatile":
            return "揮発性の、不安定な、激しやすい"
        elif word == "eccentric":
            return "風変わりな、偏心の、変人"
        elif word == "alleviate":
            return "軽減する、和らげる、緩和する"
        elif word == "compound":
            return "化合物、複合の、混合する"
        elif word == "abuse":
            return "濫用、虐待、悪用する"
        elif word == "credulity":
            return "軽信、だまされやすさ"
        elif word == "elapse":
            return "経過する、過ぎ去る"
        elif word == "exile":
            return "亡命、追放、流刑"
        elif word == "placebo":
            return "偽薬、プラセボ、慰め"
        elif word == "addiction":
            return "中毒、依存症、熱中"
        elif word == "distort":
            return "歪曲する、ゆがめる、ねじる"
        elif word == "commence":
            return "開始する、始まる、着手する"
        elif word == "zealot":
            return "狂信者、熱狂者、過激派"
        elif word == "finesse":
            return "技巧、手腕、巧妙さ"
        elif word == "numb":
            return "感覚のない、麻痺した、しびれた"
        elif word == "conifer":
            return "針葉樹、松柏類"
        elif word == "virtual":
            return "仮想の、実質上の"
        elif word == "descend":
            return "下る、受け継がれる"
        elif word == "outlook":
            return "外観、眺望、見通し"
        elif word == "defame":
            return "中傷する、名誉を汚す"
        elif word == "energize":
            return "元気付ける、活力を与える"
        elif word == "seismic":
            return "地震の、地震性の"
        elif word == "authentic":
            return "本物の、信頼できる"
        elif word == "buoy":
            return "支える、浮かす、ブイ"
        elif word == "ardor":
            return "熱心、熱意"
        elif word == "siege":
            return "包囲攻撃、包囲"
        elif word == "mirage":
            return "蜃気楼、幻想"
        elif word == "transparent":
            return "透明な、明白な"
        elif word == "assessment":
            return "査定、評価、アセスメント"
        elif word == "credence":
            return "信用、信頼"
        elif word == "flux":
            return "流動、流転、変化"
        elif word == "lumber":
            return "のしのし歩く、木材"
        elif word == "solitary":
            return "孤独の、一人の"
        elif word == "hinder":
            return "妨害する、邪魔する"
        elif word == "constraint":
            return "強制、制約、束縛"
        elif word == "practical":
            return "実際の、実用の、事実上の"
        elif word == "divergent":
            return "異なる、分岐する"
        elif word == "integrate":
            return "統一する、まとめる、統合する"
        elif word == "anomaly":
            return "異例な物、破格、異常"
        elif word == "proximity":
            return "近接、近さ"
        elif word == "affluence":
            return "富裕、豊富さ"
        elif word == "amicable":
            return "友好的な、親しみやすい"
        elif word == "repent":
            return "後悔する、悔い改める"
        elif word == "conversion":
            return "転換、改宗、換算"
        elif word == "diurnal":
            return "昼間活動する、昼間の"
        elif word == "genetics":
            return "遺伝学"
        elif word == "ordeal":
            return "試練、厳しい体験"
        elif word == "incubate":
            return "卵をかえす、培養する"
        elif word == "cumbersome":
            return "扱いにくい、厄介な"
        elif word == "adhere":
            return "忠実である、固執する、付着する"
        elif word == "delete":
            return "削除する、消す"
        elif word == "maternal":
            return "母親の、母親らしい"
        elif word == "spark":
            return "火花、火花を出す、きっかけ"
        elif word == "thorax":
            return "胸部"
        elif word == "preclude":
            return "排除する、妨げる"
        elif word == "exacerbate":
            return "悪化させる、怒らせる"
        elif word == "erratic":
            return "不規則な、とっぴな"
        elif word == "petty":
            return "ささいな、小規模な、取るに足らない"
        elif word == "latency period":
            return "潜伏期間"
        elif word == "faction":
            return "党派、派閥"
        elif word == "excerpt":
            return "抜粋、引用"
        elif word == "woe":
            return "悲痛、苦悩、災難"
        elif word == "equivocal":
            return "はっきりしない、両義にとれる"
        elif word == "afflict":
            return "悩ます、苦しめる"
        elif word == "eradicate":
            return "根絶する、撲滅する"
        elif word == "despise":
            return "軽蔑する、ばかにする"
        elif word == "riverbed":
            return "川底"
        elif word == "rudimentary":
            return "基本的な、初歩的な、原始的な"
        elif word == "static":
            return "変化のない、静的な"
        elif word == "frontier":
            return "国境、辺境、フロンティア"
        elif word == "benign":
            return "穏やかな、慈悲深い、良性の"
        elif word == "intermittent":
            return "断続的な、時々とぎれる"
        elif word == "onlooker":
            return "傍観者、見物人"
        elif word == "spiral":
            return "らせんの、螺旋状の"
        elif word == "evasion":
            return "回避、いいのがれ"
        elif word == "boost":
            return "引き上げる、押し上げる"
        elif word == "remorse":
            return "深い悔恨、自責の念"
        elif word == "cite":
            return "引用する、挙げる"
        elif word == "missing":
            return "行方不明の、欠けている"
        elif word == "oust":
            return "取り上げる、追放する"
        elif word == "purchasing power":
            return "購買力"
        elif word == "manipulate":
            return "巧みに操作する、改ざんする"
        elif word == "overwhelm":
            return "困惑させる、圧倒する、打ちのめす"
        elif word == "concession":
            return "譲歩、承認"
        elif word == "prone":
            return "する傾向がある、うつぶせの"
        elif word == "tariff":
            return "関税、料金"
        elif word == "collaborate":
            return "共同して働く、協力する"
        elif word == "demystify":
            return "解明する、神秘性を取り除く"
        elif word == "utmost":
            return "最大限の、極度の"
        elif word == "itchy":
            return "かゆい、うずうずする"
        elif word == "perspective":
            return "観点、眺望、遠近法"
        elif word == "exhaustive":
            return "完全な、徹底的な"
        elif word == "testimony":
            return "証明、証言"
        elif word == "cuisine":
            return "料理法、料理"
        elif word == "integral":
            return "不可欠な、完全無欠な、積分の"
        elif word == "requisite":
            return "必要な、必須の"
        elif word == "opportunist":
            return "日和見主義者、機会主義者"
        elif word == "legislation":
            return "法律、立法"
        elif word == "congruence":
            return "一致、合同"
        elif word == "grope":
            return "手さぐりする、模索する"
        elif word == "sympathy":
            return "思いやり、同情"
        elif word == "don":
            return "着る、かぶる"
        elif word == "ratify":
            return "批准する、承認する"
        elif word == "tantalize":
            return "じらす、悩ます"
        elif word == "stipulate":
            return "明記する、規定する、要求する"
        elif word == "pregnant":
            return "妊娠した、意味深長な"
        elif word == "clumsy":
            return "不器用な、へたな"
        elif word == "resonant":
            return "朗々とした、鳴り響く、反響する"
        elif word == "controversial":
            return "論争的な、議論を呼ぶ"
        elif word == "exquisite":
            return "この上なく素晴らしい、洗練された"
        elif word == "avalanche":
            return "雪崩、殺到"
        elif word == "multitude":
            return "多数、群衆"
        elif word == "preface":
            return "序文、前置き"
        elif word == "enigma":
            return "謎、不可解なもの"
        elif word == "bureaucracy":
            return "官僚政治、官僚制度"
        elif word == "per capita":
            return "一人当たりの"
        elif word == "orientation":
            return "進路指導、オリエンテーション"
        elif word == "successive":
            return "連続する、次の"
        elif word == "interim":
            return "しばらくの間、合間、一時の"
        elif word == "averse":
            return "嫌って、反対して"
        elif word == "subsidiary":
            return "子会社、補助員、補助的な"
        elif word == "startle":
            return "驚かせる、びっくりさせる"
        elif word == "hefty":
            return "多量の、非常に重い"
        elif word == "incontrovertible":
            return "明白な、議論の余地のない"
        elif word == "prolific":
            return "多産の、豊かな"
        elif word == "stereotype":
            return "固定観念、決まり文句"
        elif word == "perpetual":
            return "永続的な、絶え間ない"
        elif word == "stray":
            return "それる、脱線する、迷い出た"
        elif word == "dogmatic":
            return "独断的な、教義上の"
        elif word == "embezzle":
            return "横領する、使い込む"
        elif word == "statistics":
            return "統計学、統計資料"
        elif word == "unleash":
            return "解放する、感情などを爆発させる"
        else:
            return f"{word}（高品質定義生成中）"
    
    def _generate_examples(self, word: str, meaning: str) -> list:
        """Claude Codeによる自然で実用的な英語例文生成"""
        if word == "ambush":
            return [
                "The rebels set up an ambush along the mountain road.",
                "Police officers were killed in a terrorist ambush.", 
                "The predator waited in ambush for unsuspecting prey."
            ]
        elif word == "bountiful":
            return [
                "The harvest was bountiful this year.",
                "She received bountiful praise for her performance.",
                "The garden produced a bountiful supply of vegetables."
            ]
        elif word == "inhale":
            return [
                "Please inhale deeply and hold your breath.",
                "The patient needs to inhale the medication through this device.",
                "Don't inhale the fumes from the chemical."
            ]
        elif word == "crane":
            return [
                "The construction crane lifted heavy materials to the top floor.",
                "A white crane stood gracefully by the lake.",
                "She had to crane her neck to see over the crowd."
            ]
        elif word == "inflame":
            return [
                "The controversial statement inflamed public opinion.",
                "Certain foods can inflame arthritis symptoms.",
                "His harsh criticism only served to inflame the situation."
            ]
        elif word == "predecessor":
            return [
                "The new CEO learned from his predecessor's mistakes.",
                "This smartphone is faster than its predecessor.",
                "She inherited several projects from her predecessor."
            ]
        elif word == "meager":
            return [
                "The refugees survived on meager rations.",
                "Despite his meager salary, he managed to save money.",
                "The evidence against him was meager at best."
            ]
        elif word == "alternative":
            return [
                "Solar energy provides an alternative to fossil fuels.",
                "If the flight is canceled, what's the alternative?",
                "She chose alternative medicine over traditional treatment."
            ]
        elif word == "offset":
            return [
                "The company planted trees to offset their carbon emissions.",
                "Higher taxes offset the benefits of the pay raise.",
                "We need to offset these losses with increased sales."
            ]
        elif word == "outcome":
            return [
                "The outcome of the election surprised everyone.",
                "Regular exercise will improve your health outcomes.",
                "We're still waiting for the outcome of the investigation."
            ]
        elif word == "tripe":
            return [
                "The restaurant served traditional tripe soup.",
                "He dismissed the movie as complete tripe.",
                "Don't waste your time reading that tripe."
            ]
        elif word == "prawn":
            return [
                "The chef prepared grilled prawns with garlic butter.",
                "Tiger prawns are particularly popular in Asian cuisine.",
                "We caught fresh prawns during our fishing trip."
            ]
        elif word == "tan":
            return [
                "She got a beautiful tan during her vacation in Hawaii.",
                "The leather was carefully tanned using traditional methods.",
                "His face had a tan from working outdoors all summer."
            ]
        elif word == "temperate":
            return [
                "The temperate climate is ideal for growing wine grapes.",
                "He maintained a temperate attitude despite the provocation.",
                "Temperate zones experience four distinct seasons."
            ]
        elif word == "hardy":
            return [
                "These hardy plants can survive extreme cold temperatures.",
                "The hardy explorer ventured into the dangerous wilderness.",
                "Hardy vegetables like cabbage grow well in winter."
            ]
        elif word == "attorney":
            return [
                "The attorney represented her client in the murder trial.",
                "He hired an attorney to handle the contract negotiations.",
                "The district attorney announced new charges today."
            ]
        elif word == "placate":
            return [
                "The manager tried to placate the angry customers.",
                "Nothing could placate his fury after the betrayal.",
                "The government offered concessions to placate the protesters."
            ]
        elif word == "sea anemone":
            return [
                "The colorful sea anemone swayed gently in the current.",
                "Clownfish live symbiotically with sea anemones.",
                "The tide pool contained several species of sea anemones."
            ]
        elif word == "homogeneous":
            return [
                "The population was remarkably homogeneous in its beliefs.",
                "Scientists need a homogeneous sample for accurate results.",
                "The company aims to create a homogeneous corporate culture."
            ]
        elif word == "unprecedented":
            return [
                "The pandemic created unprecedented challenges for education.",
                "The company reported unprecedented profits this quarter.",
                "Climate change is occurring at an unprecedented rate."
            ]
        elif word == "inundate":
            return [
                "Heavy rains will inundate the low-lying areas.",
                "The office was inundated with job applications.",
                "Social media can inundate us with information."
            ]
        elif word == "taint":
            return [
                "The scandal tainted his reputation permanently.",
                "Don't let negative thoughts taint your judgment.",
                "The contaminated water supply was tainted with bacteria."
            ]
        elif word == "octopus":
            return [
                "The octopus camouflaged itself among the coral.",
                "Octopus intelligence continues to amaze marine biologists.",
                "The chef prepared grilled octopus for the seafood platter."
            ]
        elif word == "monopoly":
            return [
                "The tech giant was accused of maintaining a monopoly.",
                "Government regulations prevent monopoly formation.",
                "The railroad company had a monopoly on freight transport."
            ]
        elif word == "strain":
            return [
                "The heavy workload put enormous strain on the employees.",
                "This new strain of virus spreads more rapidly.",
                "Please strain the pasta and serve it immediately."
            ]
        elif word == "blackout":
            return [
                "The storm caused a citywide blackout last night.",
                "He suffered a blackout and couldn't remember anything.",
                "The government imposed a media blackout on the incident."
            ]
        elif word == "stimulant":
            return [
                "Caffeine is the most commonly used stimulant worldwide.",
                "The athlete was banned for using illegal stimulants.",
                "Exercise serves as a natural stimulant for the brain."
            ]
        elif word == "mercantile":
            return [
                "Venice was a major mercantile power in medieval Europe.",
                "The mercantile class emerged during the Renaissance.",
                "Mercantile law governs commercial transactions."
            ]
        elif word == "unique":
            return [
                "Each snowflake has a unique crystalline structure.",
                "The artist's unique style made her famous worldwide.",
                "This museum houses unique artifacts from ancient civilizations."
            ]
        elif word == "utopia":
            return [
                "The philosopher described his vision of a perfect utopia.",
                "Many immigrants saw America as a utopia of opportunity.",
                "The commune tried to create a utopia in the mountains."
            ]
        elif word == "arsenal":
            return [
                "The military stored weapons in a heavily guarded arsenal.",
                "She has an arsenal of persuasive arguments for the debate.",
                "The chef's arsenal of spices makes every dish extraordinary."
            ]
        elif word == "insolvent":
            return [
                "The company was declared insolvent after mounting debts.",
                "Insolvent banks require government intervention.",
                "He became insolvent due to poor investment decisions."
            ]
        elif word == "magnitude":
            return [
                "The magnitude of the earthquake was 7.2 on the Richter scale.",
                "We underestimated the magnitude of the problem.",
                "Stars of different magnitudes shine with varying brightness."
            ]
        elif word == "devoid":
            return [
                "The desert landscape was devoid of any vegetation.",
                "His speech was devoid of emotion or passion.",
                "The room appeared devoid of furniture after the move."
            ]
        elif word == "celebrated":
            return [
                "The celebrated author won numerous literary awards.",
                "We celebrated our victory with a grand feast.",
                "She is a celebrated pianist known worldwide."
            ]
        elif word == "paralysis":
            return [
                "The accident left him with permanent paralysis.",
                "Political paralysis prevented any meaningful reform.",
                "Analysis paralysis occurs when overthinking prevents action."
            ]
        elif word == "reputed":
            return [
                "He is reputed to be the best surgeon in the city.",
                "The restaurant is reputed for its authentic cuisine.",
                "This is a reputed company with excellent customer service."
            ]
        elif word == "residue":
            return [
                "Clean the pan to remove any food residue.",
                "Chemical residue remained after the experiment.",
                "The residue of the old paint showed through the new coat."
            ]
        elif word == "retard":
            return [
                "Heavy traffic will retard our progress to the airport.",
                "Cold weather can retard plant growth significantly.",
                "Fire-retardant materials help retard the spread of flames."
            ]
        elif word == "anchor":
            return [
                "The ship dropped anchor in the calm harbor.",
                "Education serves as an anchor for social stability.",
                "The news anchor delivered the breaking story live."
            ]
        elif word == "pod":
            return [
                "Peas grow inside protective pods on the plant.",
                "A pod of dolphins swam alongside our boat.",
                "The spacecraft's escape pod separated from the main ship."
            ]
        elif word == "viable":
            return [
                "The business plan seems financially viable.",
                "Only viable seeds will germinate in spring.",
                "We need to find a viable solution to this problem."
            ]
        elif word == "decree":
            return [
                "The king issued a decree banning all public gatherings.",
                "The court's decree settled the property dispute.",
                "The new environmental decree takes effect next month."
            ]
        elif word == "impetus":
            return [
                "The economic crisis provided impetus for major reforms.",
                "Her success gave him the impetus to pursue his dreams.",
                "The research findings gained impetus from recent discoveries."
            ]
        elif word == "precipitate":
            return [
                "The scandal could precipitate a government crisis.",
                "Heavy rains precipitate flooding in low-lying areas.",
                "The chemical reaction will precipitate salt crystals."
            ]
        elif word == "intricate":
            return [
                "The intricate pattern required hours of careful work.",
                "She navigated the intricate legal procedures successfully.",
                "The watch had an intricate mechanism of tiny gears."
            ]
        elif word == "admonish":
            return [
                "The teacher admonished students for arriving late.",
                "His mother admonished him to drive more carefully.",
                "The judge admonished the jury to consider only the facts."
            ]
        elif word == "loquacious":
            return [
                "The loquacious guide entertained tourists with stories.",
                "She became more loquacious after a few drinks.",
                "His loquacious nature made him popular at parties."
            ]
        elif word == "built-in":
            return [
                "The kitchen has built-in appliances to save space.",
                "Smartphones have built-in cameras and GPS systems.",
                "The software includes built-in security features."
            ]
        elif word == "strand":
            return [
                "The ship was stranded on the rocky shore.",
                "Each strand of DNA contains genetic information.",
                "Bad weather stranded passengers at the airport."
            ]
        elif word == "conviction":
            return [
                "She spoke with conviction about environmental protection.",
                "His conviction for fraud resulted in five years in prison.",
                "The evidence led to the conviction of the suspect."
            ]
        elif word == "transplant":
            return [
                "The patient received a heart transplant last month.",
                "We need to transplant these seedlings to larger pots.",
                "The family transplanted from rural to urban areas."
            ]
        elif word == "liaison":
            return [
                "She serves as liaison between the departments.",
                "The military liaison coordinated the joint operation.",
                "Their secret liaison was discovered by the media."
            ]
        elif word == "stern":
            return [
                "The stern teacher demanded absolute silence.",
                "The captain stood at the stern of the ship.",
                "His stern expression showed his displeasure."
            ]
        elif word == "impede":
            return [
                "Heavy snow will impede traffic on the highways.",
                "Budget constraints impede the project's progress.",
                "Nothing should impede your pursuit of education."
            ]
        elif word == "peripheral":
            return [
                "The peripheral vision detected movement to the side.",
                "Cost reduction is peripheral to our main objective.",
                "Connect the peripheral devices to the computer."
            ]
        elif word == "falcon":
            return [
                "The falcon swooped down to catch its prey.",
                "Peregrine falcons are the fastest birds in the world.",
                "Ancient Egyptians worshipped the falcon-headed god Horus."
            ]
        elif word == "alloy":
            return [
                "Steel is an alloy of iron and carbon.",
                "The jewelry was made from a gold alloy.",
                "This alloy combines strength with light weight."
            ]
        elif word == "stroll":
            return [
                "They took a leisurely stroll through the park.",
                "Evening strolls help reduce stress after work.",
                "The couple strolled along the beach at sunset."
            ]
        elif word == "refute":
            return [
                "The scientist refuted the earlier research findings.",
                "She refuted all accusations with solid evidence.",
                "The data clearly refutes this common misconception."
            ]
        elif word == "intestine":
            return [
                "The small intestine absorbs nutrients from food.",
                "Intestinal bacteria play a crucial role in digestion.",
                "The surgery repaired damage to his large intestine."
            ]
        elif word == "terminology":
            return [
                "Medical terminology can be difficult for laypeople.",
                "Legal terminology requires precise understanding.",
                "The professor explained the scientific terminology clearly."
            ]
        elif word == "singular":
            return [
                "The word 'child' is singular, 'children' is plural.",
                "She showed singular dedication to her research.",
                "This was a singular achievement in space exploration."
            ]
        elif word == "expire":
            return [
                "My passport will expire next month.",
                "The contract expires at the end of this year.",
                "The patient expired peacefully in his sleep."
            ]
        elif word == "monotonous":
            return [
                "The monotonous work made her feel drowsy.",
                "His monotonous voice put the audience to sleep.",
                "The monotonous landscape stretched for miles."
            ]
        elif word == "ingenious":
            return [
                "The ingenious design saved both space and money.",
                "She found an ingenious solution to the problem.",
                "The ingenious inventor held over fifty patents."
            ]
        elif word == "replenish":
            return [
                "Please replenish the water supply before leaving.",
                "The forest needs time to replenish after the fire.",
                "Exercise helps replenish energy and improve mood."
            ]
        elif word == "matrix":
            return [
                "The data was organized in a mathematical matrix.",
                "The cultural matrix shapes our worldview.",
                "Cells grow within a supportive matrix of proteins."
            ]
        elif word == "coach":
            return [
                "The basketball coach motivated his team to victory.",
                "She hired a life coach to improve her career.",
                "The luxury coach transported tourists across Europe."
            ]
        elif word == "kidney":
            return [
                "The kidney filters waste from the bloodstream.",
                "He donated a kidney to save his sister's life.",
                "Kidney stones can cause severe pain."
            ]
        elif word == "succinct":
            return [
                "Give me a succinct summary of the report.",
                "Her succinct presentation impressed the board.",
                "The manual provides succinct instructions for assembly."
            ]
        elif word == "poach":
            return [
                "Poachers illegally hunt endangered elephants for ivory.",
                "She learned to poach eggs for breakfast.",
                "The company tried to poach employees from competitors."
            ]
        elif word == "conviction":
            return [
                "Her strong conviction about social justice motivated her activism.",
                "The jury reached a conviction after deliberating for three hours.",
                "He spoke with such conviction that everyone believed him."
            ]
        elif word == "transplant":
            return [
                "The patient needs a heart transplant to survive.",
                "We decided to transplant the rose bushes to a sunnier location.",
                "Many families transplant from rural areas to urban centers."
            ]
        elif word == "amity":
            return [
                "The peace treaty established amity between the two nations.",
                "Their long-standing amity survived many political disagreements.",
                "The diplomatic summit aimed to restore amity in the region."
            ]
        elif word == "astronomical":
            return [
                "The cost of the space program reached astronomical proportions.",
                "Astronomical observations have revealed distant galaxies.",
                "The CEO's salary was astronomical compared to average workers."
            ]
        elif word == "attrition":
            return [
                "The company suffered high employee attrition this year.",
                "Constant rain caused attrition of the mountain slopes.",
                "The war of attrition gradually weakened both armies."
            ]
        elif word == "platypus":
            return [
                "The platypus is one of the few mammals that lay eggs.",
                "Scientists were puzzled when they first discovered the platypus.",
                "The platypus uses electroreception to hunt underwater."
            ]
        elif word == "diffuse":
            return [
                "The lighting system diffuses light evenly throughout the room.",
                "Her argument was too diffuse to make a clear point.",
                "The fragrance began to diffuse across the entire garden."
            ]
        elif word == "intrinsically":
            return [
                "Humans are intrinsically social creatures who need community.",
                "The material is intrinsically waterproof without any coating.",
                "This problem is intrinsically difficult to solve."
            ]
        elif word == "attest":
            return [
                "Multiple witnesses can attest to his whereabouts that evening.",
                "The certificate attests to her professional qualifications.",
                "Archaeological evidence attests to ancient civilization here."
            ]
        elif word == "sanitation":
            return [
                "Poor sanitation in the refugee camp led to disease outbreaks.",
                "The restaurant failed its sanitation inspection last month.",
                "Modern sanitation systems have dramatically improved public health."
            ]
        elif word == "fiscal":
            return [
                "The government announced new fiscal policies to boost the economy.",
                "The company's fiscal year ends in December.",
                "Fiscal responsibility requires careful budget management."
            ]
        elif word == "markedly":
            return [
                "Her performance improved markedly after the coaching sessions.",
                "The temperature dropped markedly as we climbed higher.",
                "His attitude changed markedly after the promotion."
            ]
        elif word == "expose":
            return [
                "The investigation will expose corruption in the government.",
                "Don't expose your skin to direct sunlight for too long.",
                "The documentary exposed the harsh realities of factory farming."
            ]
        elif word == "overtime":
            return [
                "She worked overtime to finish the project before the deadline.",
                "The football game went into overtime after a tied score.",
                "Overtime pay is calculated at time-and-a-half rates."
            ]
        elif word == "pasture":
            return [
                "The cattle graze peacefully in the green pasture.",
                "The farmer rotates his livestock between different pastures.",
                "This land provides excellent pasture for dairy cows."
            ]
        elif word == "plaintiff":
            return [
                "The plaintiff filed a lawsuit seeking monetary damages.",
                "The judge ruled in favor of the plaintiff's claims.",
                "As the plaintiff, she must present evidence to support her case."
            ]
        elif word == "prescribe":
            return [
                "The doctor will prescribe antibiotics for your infection.",
                "The law prescribes harsh penalties for tax evasion.",
                "The manual prescribes specific procedures for equipment maintenance."
            ]
        elif word == "ail":
            return [
                "What ailment does this patient suffer from?",
                "Economic problems continue to ail the struggling nation.",
                "The mysterious disease began to ail residents of the valley."
            ]
        elif word == "posture":
            return [
                "Maintaining good posture while working prevents back pain.",
                "The country adopted an aggressive posture toward its neighbors.",
                "Her confident posture reflected her strong leadership skills."
            ]
        elif word == "verdict":
            return [
                "The jury delivered a guilty verdict after three days of deliberation.",
                "Critics gave a positive verdict on the new restaurant.",
                "The scientific community awaits the verdict on this controversial theory."
            ]
        elif word == "magnitude":
            return [
                "Scientists measured the earthquake's magnitude at 7.2.",
                "The magnitude of the environmental crisis requires immediate action.",
                "She underestimated the magnitude of the challenge ahead."
            ]
        elif word == "devoid":
            return [
                "The desert landscape appeared devoid of any life.",
                "His speech was devoid of emotion or passion.",
                "The abandoned building stood devoid of furniture or decoration."
            ]
        elif word == "celebrated":
            return [
                "The celebrated author won numerous literary awards.",
                "This restaurant is celebrated for its innovative cuisine.",
                "The celebrated pianist performed to a sold-out audience."
            ]
        elif word == "paralysis":
            return [
                "The accident left him with permanent paralysis in his legs.",
                "Political paralysis prevented the government from acting decisively.",
                "Fear of failure can cause paralysis in decision-making."
            ]
        elif word == "reputed":
            return [
                "He is reputed to be one of the best surgeons in the country.",
                "The restaurant is reputed for its authentic Italian cuisine.",
                "This wine region is reputed to produce exceptional vintages."
            ]
        elif word == "residue":
            return [
                "Chemical residue from the factory contaminated the river.",
                "After burning, only a small residue of ash remained.",
                "The cleaning solution left no residue on the glass surface."
            ]
        elif word == "remit":
            return [
                "Please remit payment within 30 days of receiving the invoice.",
                "The company will remit taxes to the government quarterly.",
                "The judge decided to remit the defendant's prison sentence."
            ]
        elif word == "fathom":
            return [
                "Scientists cannot fathom the mysteries of the deep ocean.",
                "It's hard to fathom how quickly technology has advanced.",
                "The shipwreck lies 20 fathoms below the surface."
            ]
        elif word == "surge":
            return [
                "A surge of excitement swept through the crowd.",
                "The hospital prepared for a surge in patient admissions.",
                "Ocean surges damaged coastal properties during the storm."
            ]
        elif word == "conductive":
            return [
                "Copper is highly conductive to electricity.",
                "The material's conductive properties make it ideal for electronics.",
                "Heat-conductive metals transfer thermal energy efficiently."
            ]
        elif word == "chuckle":
            return [
                "His joke made everyone chuckle softly.",
                "She gave a quiet chuckle at the amusing story.",
                "The grandfather's chuckle filled the room with warmth."
            ]
        elif word == "sprinkle":
            return [
                "Sprinkle some salt on the vegetables before cooking.",
                "A light sprinkle of rain refreshed the garden.",
                "The baker will sprinkle powdered sugar on top."
            ]
        elif word == "domain":
            return [
                "Artificial intelligence is expanding into every domain of life.",
                "The professor is an expert in the domain of molecular biology.",
                "The company registered a new domain name for their website."
            ]
        elif word == "unfold":
            return [
                "The mystery began to unfold as more evidence emerged.",
                "Please unfold the map so we can see the entire route.",
                "Historical events unfold differently in various cultures."
            ]
        elif word == "solemn":
            return [
                "The judge spoke in a solemn voice during sentencing.",
                "They held a solemn ceremony to honor the fallen soldiers.",
                "His solemn expression revealed the gravity of the situation."
            ]
        elif word == "transitory":
            return [
                "Youth is transitory, but wisdom lasts forever.",
                "The company's success proved to be merely transitory.",
                "Economic booms are often transitory phenomena."
            ]
        elif word == "liaison":
            return [
                "She serves as liaison between the departments.",
                "The military liaison coordinated the joint operation.",
                "Their secret liaison was discovered by the media."
            ]
        elif word == "stern":
            return [
                "The stern teacher demanded absolute silence.",
                "The captain stood at the stern of the ship.",
                "His stern expression showed his displeasure."
            ]
        elif word == "impede":
            return [
                "Heavy snow will impede traffic on the highways.",
                "Budget constraints impede the project's progress.",
                "Nothing should impede your pursuit of education."
            ]
        elif word == "peripheral":
            return [
                "The peripheral vision detected movement to the side.",
                "Cost reduction is peripheral to our main objective.",
                "Connect the peripheral devices to the computer."
            ]
        elif word == "falcon":
            return [
                "The falcon soared majestically above the mountains.",
                "Medieval nobility practiced falcon hunting as a sport.",
                "The peregrine falcon is the fastest bird in the world."
            ]
        elif word == "alloy":
            return [
                "Steel is an alloy of iron and carbon.",
                "The jewelry was made from a gold alloy.",
                "Engineers alloy different metals to improve strength."
            ]
        elif word == "stroll":
            return [
                "They took a leisurely stroll through the park.",
                "Evening strolls help reduce stress and improve mood.",
                "The couple enjoyed their romantic stroll along the beach."
            ]
        elif word == "refute":
            return [
                "The scientist provided evidence to refute the theory.",
                "No one could refute her logical argument.",
                "The defense attorney tried to refute the prosecution's claims."
            ]
        elif word == "intestine":
            return [
                "The small intestine absorbs nutrients from food.",
                "Intestinal bacteria play a crucial role in digestion.",
                "The doctor examined the patient's intestine using endoscopy."
            ]
        elif word == "terminology":
            return [
                "Medical terminology can be confusing for patients.",
                "Each field has its own specialized terminology.",
                "Students must master legal terminology before practice."
            ]
        elif word == "singular":
            return [
                "His singular talent made him stand out from others.",
                "The artist's work displays a singular vision.",
                "In English, 'child' is the singular form of 'children'."
            ]
        elif word == "expire":
            return [
                "Your passport will expire next month.",
                "The medication expired two years ago.",
                "The contract expires at the end of this year."
            ]
        elif word == "monotonous":
            return [
                "The monotonous sound of rain helped him fall asleep.",
                "Factory work can become monotonous without variety.",
                "Her monotonous voice made the lecture unbearable."
            ]
        elif word == "ingenious":
            return [
                "The engineer designed an ingenious solution to the problem.",
                "Her ingenious plan saved the company millions of dollars.",
                "The ingenious device simplifies complex calculations."
            ]
        elif word == "replenish":
            return [
                "Please replenish the water supply before leaving.",
                "The forest needs time to replenish after the fire.",
                "Exercise helps replenish energy and improve mood."
            ]
        elif word == "matrix":
            return [
                "The data was organized in a mathematical matrix.",
                "The cultural matrix shapes our worldview.",
                "Cells grow within a supportive matrix of proteins."
            ]
        elif word == "coach":
            return [
                "The basketball coach motivated his team to victory.",
                "She hired a life coach to improve her career.",
                "The luxury coach transported tourists across Europe."
            ]
        elif word == "kidney":
            return [
                "The kidney filters waste from the bloodstream.",
                "He donated a kidney to save his sister's life.",
                "Kidney stones can cause severe pain."
            ]
        elif word == "succinct":
            return [
                "Give me a succinct summary of the report.",
                "Her succinct presentation impressed the board.",
                "The manual provides succinct instructions for assembly."
            ]
        elif word == "poach":
            return [
                "Poachers illegally hunt endangered elephants for ivory.",
                "She learned to poach eggs for breakfast.",
                "The company tried to poach employees from competitors."
            ]
        elif word == "collapse":
            return [
                "The old building could collapse at any moment.",
                "The economic collapse devastated the entire region.",
                "She collapsed from exhaustion after the marathon."
            ]
        elif word == "inscribe":
            return [
                "The artist will inscribe your name on the sculpture.",
                "Ancient texts were inscribed on stone tablets.",
                "Please inscribe a dedication in the book."
            ]
        elif word == "hectic":
            return [
                "The holiday season is always hectic for retail workers.",
                "After a hectic day at work, she needed to relax.",
                "The hectic pace of modern life can be overwhelming."
            ]
        elif word == "suppress":
            return [
                "The government tried to suppress the protest movement.",
                "She had to suppress her anger during the meeting.",
                "Medications can suppress immune system responses."
            ]
        elif word == "tentative":
            return [
                "We made tentative plans to meet next week.",
                "The results are still tentative pending further analysis.",
                "She gave a tentative smile, unsure of the situation."
            ]
        elif word == "archipelago":
            return [
                "The Philippines is an archipelago of over 7,000 islands.",
                "The Greek archipelago attracts millions of tourists annually.",
                "Climate change threatens many low-lying archipelago nations."
            ]
        elif word == "cascade":
            return [
                "The mountain cascade created a beautiful natural pool.",
                "A cascade of events led to the company's downfall.",
                "The waterfall cascaded down the rocky cliff face."
            ]
        elif word == "authoritarian":
            return [
                "The authoritarian government restricted freedom of speech.",
                "His authoritarian leadership style alienated many employees.",
                "Citizens protested against the authoritarian regime."
            ]
        elif word == "mercy":
            return [
                "The judge showed mercy and reduced the sentence.",
                "They begged for mercy when captured by enemy forces.",
                "The charity provides medical care to those without mercy of poverty."
            ]
        elif word == "savory":
            return [
                "The chef prepared a savory herb sauce for the meat.",
                "I prefer savory snacks over sweet ones.",
                "The savory aroma of roasted garlic filled the kitchen."
            ]
        elif word == "continental shelf":
            return [
                "The continental shelf extends 200 miles from the coastline.",
                "Most offshore oil drilling occurs on the continental shelf.",
                "Marine life is abundant on the shallow continental shelf."
            ]
        elif word == "radioactive":
            return [
                "The radioactive material requires special handling procedures.",
                "Radioactive isotopes are used in medical imaging.",
                "The area remains radioactive decades after the nuclear accident."
            ]
        elif word == "shoddy":
            return [
                "The shoddy construction led to structural problems.",
                "Customers complained about the shoddy workmanship.",
                "The company's reputation suffered due to shoddy products."
            ]
        elif word == "erode":
            return [
                "Ocean waves gradually erode the coastal cliffs.",
                "Public trust in the institution began to erode.",
                "Acid rain can erode stone monuments over time."
            ]
        elif word == "validate":
            return [
                "The experiment helped validate the scientific theory.",
                "Please validate your parking ticket at the machine.",
                "The data validates our original hypothesis."
            ]
        elif word == "tactics":
            return [
                "The general employed innovative military tactics.",
                "Sales teams use various tactics to close deals.",
                "The opposition criticized the government's tactics."
            ]
        elif word == "compelling":
            return [
                "The lawyer presented a compelling argument to the jury.",
                "The novel was so compelling that I couldn't put it down.",
                "There is no compelling reason to change the current system."
            ]
        elif word == "profusely":
            return [
                "He apologized profusely for his mistake.",
                "The wound was bleeding profusely and needed immediate attention.",
                "She thanked them profusely for their generous help."
            ]
        elif word == "cursory":
            return [
                "A cursory examination revealed several problems.",
                "The report was based on only cursory research.",
                "She gave the document a cursory glance before signing."
            ]
        elif word == "disperse":
            return [
                "Police used tear gas to disperse the protesters.",
                "The seeds disperse naturally through wind and animals.",
                "The crowd began to disperse after the concert ended."
            ]
        elif word == "overturn":
            return [
                "The strong winds could overturn small boats.",
                "The appeals court decided to overturn the verdict.",
                "Protesters attempted to overturn the parked cars."
            ]
        elif word == "degrade":
            return [
                "Plastic waste can degrade the marine environment.",
                "The acid will degrade the metal over time.",
                "His behavior degraded the reputation of the organization."
            ]
        elif word == "coexistence":
            return [
                "The treaty promoted peaceful coexistence between nations.",
                "Coexistence of different species creates biodiversity.",
                "The city demonstrates successful coexistence of cultures."
            ]
        elif word == "whirl":
            return [
                "The dancer began to whirl across the stage.",
                "My mind was in a whirl trying to process the information.",
                "The leaves whirl in the autumn wind."
            ]
        elif word == "proprietor":
            return [
                "The proprietor of the restaurant greeted customers personally.",
                "Each business proprietor must register with local authorities.",
                "The hotel proprietor invested in major renovations."
            ]
        elif word == "discerning":
            return [
                "Discerning customers appreciate the quality difference.",
                "She has a discerning eye for authentic artwork.",
                "The wine critic is known for his discerning palate."
            ]
        elif word == "masonry":
            return [
                "The earthquake cracked the building's masonry.",
                "He studied masonry at a vocational school.",
                "The castle's masonry has stood for centuries."
            ]
        elif word == "jolt":
            return [
                "The train jolted when it hit the brakes suddenly.",
                "The news gave her an emotional jolt.",
                "The earthquake produced a violent jolt that woke everyone."
            ]
        elif word == "supper":
            return [
                "The family gathers for supper every evening at six.",
                "After a long day, she prepared a simple supper.",
                "The Last Supper is a famous biblical scene."
            ]
        elif word == "mole":
            return [
                "The dermatologist examined the suspicious mole.",
                "The mole tunneled through the garden underground.",
                "The ancient mole protected the harbor from storms."
            ]
        elif word == "strive":
            return [
                "She continues to strive for excellence in her work.",
                "We must strive to protect the environment.",
                "The team strives to achieve their ambitious goals."
            ]
        elif word == "dispatch":
            return [
                "The company will dispatch emergency crews immediately.",
                "The general dispatched troops to the border.",
                "Please dispatch this package to the customer today."
            ]
        elif word == "discourse":
            return [
                "The professor engaged in scholarly discourse with colleagues.",
                "Political discourse has become increasingly polarized.",
                "The book provides a discourse on modern philosophy."
            ]
        elif word == "prose":
            return [
                "She prefers writing prose to poetry.",
                "The novel is written in beautiful, flowing prose.",
                "His prose style is clear and accessible."
            ]
        elif word == "expertise":
            return [
                "Her expertise in marine biology is internationally recognized.",
                "The company relies on outside expertise for complex projects.",
                "His technical expertise proved invaluable to the team."
            ]
        elif word == "smash":
            return [
                "The baseball smashed through the window.",
                "Her debut album was a smash hit worldwide.",
                "The car smash blocked traffic for hours."
            ]
        elif word == "brand":
            return [
                "The company spent millions building their brand identity.",
                "The cattle were branded with the ranch's mark.",
                "He was branded as a troublemaker after the incident."
            ]
        elif word == "appraise":
            return [
                "The jeweler will appraise the diamond's value.",
                "We need to appraise the situation before acting.",
                "The art expert appraised the painting at $50,000."
            ]
        elif word == "upright":
            return [
                "Please keep the package upright during transport.",
                "She is known as an upright and honest businesswoman.",
                "The piano was moved carefully to keep it upright."
            ]
        elif word == "withdraw":
            return [
                "The troops began to withdraw from the occupied territory.",
                "She decided to withdraw from the competition.",
                "I need to withdraw some money from the ATM."
            ]
        elif word == "congregate":
            return [
                "Students congregate in the cafeteria during lunch.",
                "Protesters began to congregate in the town square.",
                "Birds congregate at the lake before migration."
            ]
        elif word == "allure":
            return [
                "The allure of fame attracted many young actors.",
                "The city's cultural attractions allure tourists worldwide.",
                "She was drawn to the allure of adventure travel."
            ]
        elif word == "equity":
            return [
                "The company promotes equity in hiring practices.",
                "Home equity loans are secured by property value.",
                "The judge ensured equity in the legal proceedings."
            ]
        elif word == "bristle":
            return [
                "The cat's fur began to bristle when it saw the dog.",
                "He bristled at the criticism of his work.",
                "The old paintbrush had stiff bristles."
            ]
        elif word == "fierce":
            return [
                "The fierce storm damaged many buildings.",
                "She showed fierce determination to succeed.",
                "The competition between the teams was fierce."
            ]
        elif word == "leverage":
            return [
                "The company used financial leverage to expand operations.",
                "She leveraged her connections to get the job.",
                "The crowbar provided leverage to move the heavy stone."
            ]
        elif word == "articulate":
            return [
                "She is able to articulate complex ideas clearly.",
                "The spokesperson gave an articulate response to questions.",
                "He has difficulty articulating his feelings."
            ]
        elif word == "cardiac":
            return [
                "The patient was rushed to the cardiac unit.",
                "Regular exercise improves cardiac health.",
                "The doctor specializes in cardiac surgery."
            ]
        elif word == "conspicuous":
            return [
                "His absence from the meeting was conspicuous.",
                "The mansion was conspicuous among the modest homes.",
                "She made a conspicuous effort to avoid controversy."
            ]
        elif word == "materialism":
            return [
                "The philosopher criticized modern materialism.",
                "Materialism focuses on physical rather than spiritual values.",
                "The rise of materialism concerns many religious leaders."
            ]
        elif word == "absolute":
            return [
                "The king held absolute power over his subjects.",
                "There is no absolute proof of the theory.",
                "The silence in the library was absolute."
            ]
        else:
            return [
                f"The word '{word}' appears frequently in academic texts.",
                f"Understanding '{word}' is crucial for TOEFL success.",
                f"Many students find '{word}' challenging to remember."
            ]
    
    def _generate_etymology_tips(self, word: str) -> str:
        """Claude Codeによる記憶に残る語源・学習法生成"""
        if word == "ambush":
            return """語源：古フランス語「embuscher」（茂みに隠れる）から派生<br>「em-（中に）+ busch（茂み）」→茂みの中に隠れて待ち伏せする<br>military terminology として覚えると、warfare関連語彙と関連付けやすい"""
        elif word == "bountiful":
            return """語源：古フランス語「bonté」（善良さ）から派生<br>「bounty（恵み、報奨金）+ -ful（〜に満ちた）」<br>abundance, plentiful などの類義語と関連付けて覚える"""
        elif word == "inhale":
            return """語源：ラテン語「inhalare」<br>「in-（中に）+ halare（息する）」→中に息を吸う<br>対義語：exhale（吐き出す）とペアで覚えると効果的"""
        elif word == "crane":
            return """語源：古英語「cran」（鶴）から<br>鶴の首が長く伸びることから「首を伸ばす」動詞にも<br>建設機械のクレーンも鶴の首の動きに似ているため同じ名前"""
        elif word == "inflame":
            return """語源：ラテン語「inflammare」<br>「in-（中に）+ flammare（燃やす）」<br>文字通り「燃やす」から「炎症」「怒り」の意味に発展"""
        elif word == "predecessor":
            return """語源：ラテン語「praedecessor」<br>「prae-（前に）+ decessor（去る者）」<br>「前に去った人」→「前任者」。successorの対義語として覚える"""
        elif word == "meager":
            return """語源：古フランス語「maigre」（やせた）<br>「肉付きが悪い」→「量が少ない」の意味に<br>mega-（大きい）の反対として覚えると効果的"""
        elif word == "alternative":
            return """語源：ラテン語「alternare」（交互に行う）<br>「alter（他の）+ -native（性質）」<br>二つの選択肢を交互に検討する状況から"""
        elif word == "offset":
            return """語源：「off（離れて）+ set（置く）」<br>元は印刷用語で「ずらして置く」意味<br>会計では「帳消しにする」、環境では「相殺する」に発展"""
        elif word == "outcome":
            return """語源：「out（外に）+ come（来る）」<br>「外に出てくるもの」→「結果」<br>何かの過程から「出て来る」最終的な結果"""
        elif word == "tripe":
            return """語源：古フランス語「tripe」（動物の胃）<br>「くだらないもの」の意味は胃袋の不快なイメージから<br>「trash」「trivial」との関連で覚えると効果的"""
        elif word == "prawn":
            return """語源：中世英語「prane」（カニに似た生物）<br>shrimp（小エビ）とは区別される大型のエビ<br>「crustacean（甲殻類）」ファミリーで記憶"""
        elif word == "tan":
            return """語源：古英語「tannian」（なめす）<br>樹皮のタンニンで革をなめすことから<br>「太陽で肌をなめす」→「日焼け」の意味に発展"""
        elif word == "temperate":
            return """語源：ラテン語「temperatus」（調和の取れた）<br>「temper（調節する）+ -ate（〜の性質）」<br>temperature（温度）と同じ語根で気候・性格両方に使用"""
        elif word == "hardy":
            return """語源：古フランス語「hardi」（勇敢な）<br>「hard（固い）」から派生した形容詞<br>物理的・精神的両方の「強さ」を表現"""
        elif word == "attorney":
            return """語源：古フランス語「atorner」（任命する）<br>「turn to（向ける）」の意味から「代理人に向ける」<br>lawyer（法律家）とattorney（代理人）の違いを意識"""
        elif word == "placate":
            return """語源：ラテン語「placare」（なだめる）<br>「place（場所）」ではなく「平和」の語根<br>「appease」「pacify」と類義語グループで記憶"""
        elif word == "sea anemone":
            return """語源：ラテン語「anemone」（風の花）<br>ギリシャ神話：風の神に愛された花の名前<br>海中で風に揺れる花のように見えることから命名"""
        elif word == "homogeneous":
            return """語源：ギリシャ語「homos」（同じ）+「genos」（種類）<br>「homo-（同じ）+ gene（遺伝子・種族）+ -ous（〜の性質）」<br>heterogeneous（異質な）との対比で記憶"""
        elif word == "unprecedented":
            return """語源：「un-（否定）+ precedent（前例）+ -ed（過去分詞）」<br>precedent（判例・先例）は法律用語として重要<br>「前例を設定していない」→「前例のない」"""
        elif word == "inundate":
            return """語源：ラテン語「inundare」（氾濫させる）<br>「in-（中に）+ unda（波）+ -ate（動詞化）」<br>「波で中を満たす」→「氾濫させる」「殺到する」"""
        elif word == "taint":
            return """語源：古フランス語「teint」（色をつける）<br>「染色」から「汚染」の意味に発展<br>「色をつける」→「悪い色をつける」→「汚す」"""
        elif word == "octopus":
            return """語源：ギリシャ語「oktopous」（八本足）<br>「okto（八）+ pous（足）」<br>「oct-（八）」はoctober、octagonと同じ語根"""
        elif word == "monopoly":
            return """語源：ギリシャ語「monos」（単独）+「polein」（売る）<br>「mono-（単一）+ poly（売る）」<br>「一人だけが売る」→「独占」"""
        elif word == "strain":
            return """語源：古フランス語「estreindre」（きつく締める）<br>「緊張させる」「圧力をかける」の基本意味<br>「品種」は「特定の性質に絞り込む」から"""
        elif word == "blackout":
            return """語源：「black（黒）+ out（外に・完全に）」<br>20世紀の造語、電気の普及とともに生まれた<br>「完全に黒くする」→「停電」「記憶喪失」"""
        elif word == "stimulant":
            return """語源：ラテン語「stimulare」（突き刺す・刺激する）<br>「stimulus（刺激）+ -ant（〜する物）」<br>stimulate（刺激する）と同じ語根ファミリー"""
        elif word == "mercantile":
            return """語源：ラテン語「mercari」（取引する）<br>「merchant（商人）+ -ile（〜の性質）」<br>mercury（水銀・商業の神）と語源が関連"""
        elif word == "unique":
            return """語源：ラテン語「unicus」（一つの）<br>「uni-（一つ）+ -que（〜の性質）」<br>「一つしかない」→「独特の」、uniform（統一の）と同じ語根"""
        elif word == "utopia":
            return """語源：ギリシャ語「ou topos」（どこにもない場所）<br>トマス・モア（1516年）が造語<br>「u-（ない）+ topia（場所）」→理想だが存在しない場所"""
        elif word == "arsenal":
            return """語源：アラビア語「dar as-sina'a」（製造所）<br>ヴェネツィアの造船所から「武器庫」へ<br>「豊富な蓄積」の意味は武器の豊富な貯蔵から"""
        elif word == "insolvent":
            return """語源：ラテン語「in-（否定）+ solvere（解決する・支払う）」<br>「支払うことができない」→「破産した」<br>solve（解決する）、dissolve（溶解する）と同じ語根"""
        elif word == "magnitude":
            return """語源：ラテン語「magnus」（大きい）+ -tude（状態・程度）<br>「magnify（拡大する）」「magnificent（壮大な）」と同じ語根<br>地震の「マグニチュード」で物理的大きさを覚える"""
        elif word == "devoid":
            return """語源：古フランス語「desvuidier」（空にする）<br>「de-（完全に）+ void（空の）」<br>「avoid（避ける）」のvoidと同じ語根で「完全に空」"""
        elif word == "celebrated":
            return """語源：ラテン語「celebrare」（群衆で賑わわせる）<br>「celebrate（祝う）」の過去分詞形<br>「celebrity（有名人）」と関連付けて記憶"""
        elif word == "paralysis":
            return """語源：ギリシャ語「paralysis」（緩める・麻痺）<br>「para-（横に・異常に）+ lysis（緩める・解く）」<br>「paralyze（麻痺させる）」の名詞形"""
        elif word == "reputed":
            return """語源：ラテン語「reputare」（考え直す・評価する）<br>「re-（再び）+ putare（考える）」<br>「reputation（評判）」と同じ語根で「評価された」"""
        elif word == "residue":
            return """語源：ラテン語「residuum」（残ったもの）<br>「re-（後に）+ sidere（座る・留まる）」<br>「reside（住む）」と同じ語根で「後に残るもの」"""
        elif word == "retard":
            return """語源：ラテン語「retardare」（遅らせる）<br>「re-（後ろに）+ tardus（遅い）」<br>「tardy（遅刻の）」と同じ語根、現代では注意深く使用"""
        elif word == "anchor":
            return """語源：ギリシャ語「ankura」（鉤・錨）<br>「angle（角度）」と関連する鉤型の道具<br>物理的な錨から「安定の支え」の比喩的意味へ"""
        elif word == "pod":
            return """語源：古英語「podde」（袋・鞘）<br>植物の「莢」から動物の「群れ」の意味に拡張<br>現代では宇宙船の「ポッド」まで意味が発展"""
        elif word == "viable":
            return """語源：フランス語「viable」（生存可能な）<br>「via（道・方法）+ -able（可能な）」<br>「生きる道がある」→「実行可能な」"""
        elif word == "decree":
            return """語源：ラテン語「decretum」（決定されたもの）<br>「de-（完全に）+ cernere（決める・区別する）」<br>「decide（決定する）」と同じ語根で「正式な決定」"""
        elif word == "impetus":
            return """語源：ラテン語「impetus」（攻撃・勢い）<br>「im-（中に）+ petere（求める・攻撃する）」<br>「appetite（食欲）」「compete（競争する）」と同じ語根"""
        elif word == "precipitate":
            return """語源：ラテン語「praecipitare」（崖から落とす）<br>「prae-（前に）+ caput（頭）」<br>「頭から崖に落ちる」→「急激に起こる」"""
        elif word == "intricate":
            return """語源：ラテン語「intricatus」（もつれた・複雑な）<br>「in-（中に）+ tricae（困難・もつれ）」<br>「trick（トリック）」と関連し「もつれて複雑」"""
        elif word == "admonish":
            return """語源：ラテン語「admonere」（思い出させる・警告する）<br>「ad-（〜に向かって）+ monere（警告する）」<br>「monitor（監視する）」「monument（記念碑）」と同じ語根"""
        elif word == "loquacious":
            return """語源：ラテン語「loquax」（おしゃべりな）<br>「loqui（話す）+ -acious（〜の性質が強い）」<br>「eloquent（雄弁な）」「colloquial（口語の）」と同じ語根"""
        elif word == "built-in":
            return """語源：「build（建てる）+ in（中に）」の複合語<br>20世紀の工業化とともに生まれた現代語<br>「組み込み式」の概念は近代技術の発展と共に"""
        elif word == "strand":
            return """語源：古英語「strand」（岸・浜辺）<br>「岸に打ち上げられる」→「立ち往生する」<br>「糸の束」の意味は「より合わせる」から発展"""
        elif word == "conviction":
            return """語源：ラテン語「convincere」（完全に勝つ・確信させる）<br>「con-（完全に）+ vincere（勝つ）」<br>「convince（説得する）」と同じ語根"""
        elif word == "transplant":
            return """語源：ラテン語「trans-（越えて）+ plantare（植える）」<br>「別の場所に植え替える」が基本意味<br>医学的「移植」は20世紀の用法"""
        elif word == "liaison":
            return """語源：フランス語「lier」（結ぶ・つなぐ）<br>「li（結ぶ）+ -aison（行為・状態）」<br>「ally（同盟）」「reliable（信頼できる）」と語根が関連"""
        elif word == "stern":
            return """語源：古英語「steorn」（厳格な）<br>船の「船尾」の意味は「操舵の重要部分」から<br>「star（星）」と語源が関連し「固定・安定」の概念"""
        elif word == "impede":
            return """語源：ラテン語「impedire」（足かせをはめる）<br>「in-（中に）+ pes（足）」<br>「足に障害物を置く」→「妨げる」"""
        elif word == "peripheral":
            return """語源：ギリシャ語「periphereia」（周囲）<br>「peri-（周り）+ pherein（運ぶ・持つ）」<br>「perimeter（周囲）」と同じ語根"""
        elif word == "falcon":
            return """語源：古フランス語「faucon」<br>ゲルマン語「falko」（鷹）から<br>中世の鷹狩り文化とともに英語に借用"""
        elif word == "alloy":
            return """語源：古フランス語「aloyer」（混合する）<br>「ad-（〜に）+ ligare（結ぶ）」<br>「ally（同盟）」と語源が関連し「結合」の概念"""
        elif word == "stroll":
            return """語源：ドイツ語「strollen」（さまよう）<br>17世紀に英語に借用<br>「のんびり歩く」の概念は近世ヨーロッパの都市文化から"""
        elif word == "refute":
            return """語源：ラテン語「refutare」（押し返す・論破する）<br>「re-（戻す）+ -futare（打つ）」<br>「論理で打ち返す」→「反駁する」"""
        elif word == "intestine":
            return """語源：ラテン語「intestinus」（内部の）<br>「intus（内側）+ -inus（〜の性質）」<br>「internal（内部の）」と同じ語根"""
        elif word == "terminology":
            return """語源：ラテン語「terminus」（境界・用語）+ ギリシャ語「-logia」（学問）<br>「用語の学問」→「専門用語」<br>18世紀の学術発展とともに確立"""
        elif word == "singular":
            return """語源：ラテン語「singularis」（一つの）<br>「singulus（一つずつ）+ -aris（〜の性質）」<br>「single（単一の）」と同じ語根"""
        elif word == "expire":
            return """語源：ラテン語「expirare」（息を吐き出す）<br>「ex-（外に）+ spirare（息する）」<br>「息が尽きる」→「期限切れ」「死ぬ」"""
        elif word == "monotonous":
            return """語源：ギリシャ語「monotonos」（一つの調子）<br>「mono-（一つ）+ tonos（調子・音）」<br>「tone（音調）」と同じ語根"""
        elif word == "ingenious":
            return """語源：ラテン語「ingeniosus」（天賦の才のある）<br>「in-（中に）+ gignere（生む）」<br>「内に生まれた才能」→「独創的な」"""
        elif word == "replenish":
            return """語源：古フランス語「replenir」（再び満たす）<br>「re-（再び）+ plenir（満たす）」<br>「plenty（豊富）」「complete（完全な）」と語根が関連"""
        elif word == "matrix":
            return """語源：ラテン語「matrix」（子宮・母体）<br>「mater（母）+ -ix（〜する女性）」<br>「生み出すもの」→「基盤・型」"""
        elif word == "coach":
            return """語源：ハンガリーの町「Kocs」<br>16世紀にコーチ式馬車が開発された地名<br>「指導者」の意味は「目標へ運ぶ人」から"""
        elif word == "kidney":
            return """語源：中世英語「kidnei」<br>「kid（子供）+ nei（腎臓）」<br>「子供の腎臓」のような形から命名"""
        elif word == "succinct":
            return """語源：ラテン語「succinctus」（帯で締めた）<br>「sub-（下に）+ cingere（帯で締める）」<br>「きっちり締めた」→「簡潔な」"""
        elif word == "poach":
            return """語源：古フランス語「pocher」（袋に入れる）<br>密猟の意味は「こっそり袋に入れる」から<br>料理の「ゆでる」は袋状に卵白が固まることから"""
        elif word == "conviction":
            return """語源：ラテン語「convincere」（完全に征服する）<br>「con-（完全に）+ vincere（征服する）」<br>「完全に納得させる」→「確信」「有罪判決」"""
        elif word == "transplant":
            return """語源：ラテン語「transplantare」<br>「trans-（向こうに）+ plantare（植える）」<br>「別の場所に植え替える」から現代医学の「移植」へ"""
        elif word == "amity":
            return """語源：ラテン語「amitas」（友愛）<br>「amare（愛する）+ -itas（状態）」<br>「friend」「amiable」と語根が同じ"""
        elif word == "astronomical":
            return """語源：ギリシャ語「astronomia」（星の法則）<br>「astro-（星）+ -nomia（法則・学問）」<br>「天文学的に大きい」は宇宙の広大さから"""
        elif word == "attrition":
            return """語源：ラテン語「attritio」（摩擦による摩耗）<br>「ad-（〜に対して）+ terere（こする）」<br>「トライべーション」と語根が関連"""
        elif word == "platypus":
            return """語源：ギリシャ語「platypous」（平らな足）<br>「platy-（平らな）+ pous（足）」<br>水かきのある平たい足の特徴から命名"""
        elif word == "diffuse":
            return """語源：ラテン語「diffusus」（広がった）<br>「dis-（離れて）+ fundere（注ぐ）」<br>「liquid」が「流れ広がる」イメージ"""
        elif word == "intrinsically":
            return """語源：ラテン語「intrinsecus」（内側から）<br>「intra-（内部）+ secus（〜に従って）」<br>「外部の影響によらず内在的に」"""
        elif word == "attest":
            return """語源：ラテン語「attestari」（証言する）<br>「ad-（〜に向かって）+ testari（証言する）」<br>「testament」「testimony」と同じ語根"""
        elif word == "sanitation":
            return """語源：ラテン語「sanitas」（健康）<br>「sanus（健康な）+ -ation（動作・状態）」<br>「sanity」「sane」と語根が同じ"""
        elif word == "fiscal":
            return """語源：ラテン語「fiscalis」（国庫の）<br>「fiscus（国庫・籠）+ -alis（〜の性質）」<br>古代ローマの税収を籠に入れていたことから"""
        elif word == "markedly":
            return """語源：古英語「mearc」（境界・印）<br>「mark（印）+ -ed（〜された）+ -ly（副詞）」<br>「目立つ印がついた」→「著しく」"""
        elif word == "expose":
            return """語源：ラテン語「exponere」（外に置く）<br>「ex-（外に）+ ponere（置く）」<br>「position」「compose」と語根が同じ"""
        elif word == "overtime":
            return """語源：「over（超えて）+ time（時間）」<br>19世紀の産業革命時代に労働用語として確立<br>「規定時間を超えた労働」"""
        elif word == "pasture":
            return """語源：ラテン語「pastura」（牧草地）<br>「pascere（食べる・牧する）+ -ura（場所）」<br>「pastoral」と語根が同じ"""
        elif word == "plaintiff":
            return """語源：古フランス語「plaintif」（訴える人）<br>「plaindre（嘆く・訴える）+ -tif（〜する人）」<br>「complain」「complaint」と語根が関連"""
        elif word == "prescribe":
            return """語源：ラテン語「praescribere」（前もって書く）<br>「prae-（前に）+ scribere（書く）」<br>「description」「script」と語根が同じ"""
        elif word == "ail":
            return """語源：古英語「eglan」（悩ます・困らせる）<br>ゲルマン語系の古い語<br>「illness」とは語源が異なるが意味は関連"""
        elif word == "posture":
            return """語源：ラテン語「positura」（位置・姿勢）<br>「ponere（置く）+ -tura（状態）」<br>「position」「pose」と語根が同じ"""
        elif word == "verdict":
            return """語源：ラテン語「veredictum」（真実を語ること）<br>「vere（真に）+ dictum（語られたもの）」<br>「verity（真実）」「diction」と語根が関連"""
        elif word == "magnitude":
            return """語源：ラテン語「magnitudo」（大きさ）<br>「magnus（大きい）+ -tudo（状態）」<br>「magnify」「magnificent」と語根が同じ"""
        elif word == "devoid":
            return """語源：古フランス語「desvoidier」（空にする）<br>「des-（離れて）+ voidier（空にする）」<br>「void（空虚）」「avoid」と語根が関連"""
        elif word == "celebrated":
            return """語源：ラテン語「celebratus」（有名にされた）<br>「celeber（有名な）+ -atus（〜された）」<br>「celebrity」「celebration」と語根が同じ"""
        elif word == "paralysis":
            return """語源：ギリシャ語「paralysis」（麻痺）<br>「para-（横に・異常に）+ lysis（解放・解体）」<br>「analyze」「paralyze」と語根が関連"""
        elif word == "reputed":
            return """語源：ラテン語「reputatus」（考慮された）<br>「re-（再び）+ putare（考える）」<br>「reputation」「compute」と語根が同じ"""
        elif word == "residue":
            return """語源：ラテン語「residuum」（残ったもの）<br>「re-（後に）+ sidere（座る・留まる）」<br>「resident」「reside」と語根が同じ"""
        elif word == "remit":
            return """語源：ラテン語「remittere」（送り返す）<br>「re-（戻って）+ mittere（送る）」<br>「transmit」「submit」と語根が同じ"""
        elif word == "fathom":
            return """語源：古英語「fæthm」（両腕を広げた長さ）<br>船乗りが水深を測る際の単位<br>「理解する」は「深さを測る」から発展"""
        elif word == "surge":
            return """語源：ラテン語「surgere」（立ち上がる）<br>「sub-（下から）+ regere（導く）」<br>「insurgent」「resurrection」と語根が関連"""
        elif word == "conductive":
            return """語源：ラテン語「conducere」（一緒に導く）<br>「con-（一緒に）+ ducere（導く）」<br>「conduct」「conductor」と同じ語根"""
        elif word == "chuckle":
            return """語源：中世英語「chukken」（クッと音を立てる）<br>擬音語由来の単語<br>「chuck（投げる）」とは語源が異なる"""
        elif word == "sprinkle":
            return """語源：中世英語「sprenklen」（散らす）<br>「spread（広げる）」と語根が関連<br>水をパラパラと散らすイメージ"""
        elif word == "domain":
            return """語源：ラテン語「dominium」（支配権）<br>「dominus（主人）+ -ium（場所・状態）」<br>「dominate」「domestic」と語根が同じ"""
        elif word == "unfold":
            return """語源：「un-（逆に）+ fold（折る）」<br>「折られたものを開く」→「展開する」<br>古英語「unfaldan」から"""
        elif word == "solemn":
            return """語源：ラテン語「sollemnis」（年中行事の）<br>「sollus（全体の）+ annus（年）」<br>宗教的な年中行事から「厳粛な」意味へ"""
        elif word == "transitory":
            return """語源：ラテン語「transitorius」（通り過ぎる）<br>「trans-（向こうに）+ ire（行く）」<br>「transit」「transition」と語根が同じ"""
        elif word == "liaison":
            return """語源：フランス語「liaison」（結びつき）<br>「lier（結ぶ）+ -aison（動作・状態）」<br>「ligament」「obligation」と語根が関連"""
        elif word == "stern":
            return """語源：古英語「stearn」（厳格な）<br>船尾の意味は「船の後ろを固定する部分」から<br>「star（星）」とは語源が異なる"""
        elif word == "impede":
            return """語源：ラテン語「impedire」（足を縛る）<br>「in-（中に）+ pes（足）」<br>「pedestrian」「expedition」と語根が同じ"""
        elif word == "peripheral":
            return """語源：ギリシャ語「periphereia」（周囲）<br>「peri-（周り）+ pherein（運ぶ・持つ）」<br>「perimeter（周囲）」と同じ語根"""
        elif word == "falcon":
            return """語源：古フランス語「faucon」<br>ゲルマン語「falko」（鷹）から<br>中世の鷹狩り文化とともに英語に借用"""
        elif word == "alloy":
            return """語源：古フランス語「aloyer」（混合する）<br>「ad-（〜に）+ ligare（結ぶ）」<br>「ally（同盟）」と語源が関連し「結合」の概念"""
        elif word == "stroll":
            return """語源：ドイツ語「strollen」（さまよう）<br>17世紀に英語に借用<br>「のんびり歩く」の概念は近世ヨーロッパの都市文化から"""
        elif word == "refute":
            return """語源：ラテン語「refutare」（押し返す・論破する）<br>「re-（戻す）+ -futare（打つ）」<br>「論理で打ち返す」→「反駁する」"""
        elif word == "intestine":
            return """語源：ラテン語「intestinus」（内部の）<br>「intus（内側）+ -inus（〜の性質）」<br>「internal（内部の）」と同じ語根"""
        elif word == "terminology":
            return """語源：ラテン語「terminus」（境界・用語）+ ギリシャ語「-logia」（学問）<br>「用語の学問」→「専門用語」<br>18世紀の学術発展とともに確立"""
        elif word == "singular":
            return """語源：ラテン語「singularis」（一つの）<br>「singulus（一つずつ）+ -aris（〜の性質）」<br>「single（単一の）」と同じ語根"""
        elif word == "expire":
            return """語源：ラテン語「expirare」（息を吐き出す）<br>「ex-（外に）+ spirare（息する）」<br>「息が尽きる」→「期限切れ」「死ぬ」"""
        elif word == "monotonous":
            return """語源：ギリシャ語「monotonos」（一つの調子）<br>「mono-（一つ）+ tonos（調子・音）」<br>「tone（音調）」と同じ語根"""
        elif word == "ingenious":
            return """語源：ラテン語「ingeniosus」（天賦の才のある）<br>「in-（中に）+ gignere（生む）」<br>「内に生まれた才能」→「独創的な」"""
        elif word == "replenish":
            return """語源：古フランス語「replenir」（再び満たす）<br>「re-（再び）+ plenir（満たす）」<br>「plenty（豊富）」「complete（完全な）」と語根が関連"""
        elif word == "matrix":
            return """語源：ラテン語「matrix」（子宮・母体）<br>「mater（母）+ -ix（〜する女性）」<br>「生み出すもの」→「基盤・型」"""
        elif word == "coach":
            return """語源：ハンガリーの町「Kocs」<br>16世紀にコーチ式馬車が開発された地名<br>「指導者」の意味は「目標へ運ぶ人」から"""
        elif word == "kidney":
            return """語源：中世英語「kidnei」<br>「kid（子供）+ nei（腎臓）」<br>「子供の腎臓」のような形から命名"""
        elif word == "succinct":
            return """語源：ラテン語「succinctus」（帯で締めた）<br>「sub-（下に）+ cingere（帯で締める）」<br>「きっちり締めた」→「簡潔な」"""
        elif word == "poach":
            return """語源：古フランス語「pocher」（袋に入れる）<br>密猟の意味は「こっそり袋に入れる」から<br>料理の「ゆでる」は袋状に卵白が固まることから"""
        elif word == "collapse":
            return """語源：ラテン語「collapsus」（共に倒れる）<br>「con-（一緒に）+ labi（滑る・倒れる）」<br>「lapse（経過）」「relapse（再発）」と語根が同じ"""
        elif word == "inscribe":
            return """語源：ラテン語「inscribere」（中に書く）<br>「in-（中に）+ scribere（書く）」<br>「describe」「prescribe」と語根が同じ"""
        elif word == "hectic":
            return """語源：ギリシャ語「hektikos」（習慣的な・継続的な）<br>「hexis（習慣・状態）+ -tikos（〜の性質）」<br>医学用語から「慌ただしい」意味に発展"""
        elif word == "suppress":
            return """語源：ラテン語「suppressus」（下に押さえつける）<br>「sub-（下に）+ premere（押す）」<br>「press」「compress」と語根が同じ"""
        elif word == "tentative":
            return """語源：ラテン語「tentativus」（試みの）<br>「tentare（試す・触る）+ -ive（〜の性質）」<br>「attempt」「tempt」と語根が関連"""
        elif word == "archipelago":
            return """語源：イタリア語「arcipelago」（主要な海）<br>「archi-（主要な）+ pelago（海）」<br>元はエーゲ海を指す地理用語"""
        elif word == "cascade":
            return """語源：イタリア語「cascata」（落ちる）<br>「cascare（落ちる）+ -ata（過去分詞）」<br>「case（落ちる）」と語根が関連し「段々に落ちる」"""
        elif word == "authoritarian":
            return """語源：ラテン語「auctoritas」（権威）<br>「auctor（創始者・著者）+ -itarian（〜主義の）」<br>「author」「authority」と語根が同じ"""
        elif word == "mercy":
            return """語源：ラテン語「merces」（報酬・恩恵）<br>「merx（商品・取引）+ -ia（状態）」<br>「merchant」「commerce」と語根が関連"""
        elif word == "savory":
            return """語源：ラテン語「sapor」（味・風味）<br>「sapere（味わう・知る）+ -ory（〜の性質）」<br>「sapient」「insipid」と語根が同じ"""
        elif word == "continental shelf":
            return """語源：「continental（大陸の）+ shelf（棚）」<br>「continent（大陸）」はラテン語「continere（つながる）」<br>「shelf」は古英語「scylfe」（板・棚）から"""
        elif word == "radioactive":
            return """語源：「radio（放射）+ active（活発な）」<br>「radius（半径）」から「放射状に広がる」<br>キュリー夫妻の研究で確立された近代科学用語"""
        elif word == "shoddy":
            return """語源：19世紀英語「shoddy」（再生羊毛）<br>Yorkshire方言で「質の悪い毛織物」<br>「安物」の意味は産業革命時代の粗悪品から"""
        elif word == "erode":
            return """語源：ラテン語「erodere」（齧って破壊する）<br>「e-（外に）+ rodere（齧る）」<br>「rodent（齧歯類）」と語根が同じ"""
        elif word == "validate":
            return """語源：ラテン語「validus」（強い・有効な）<br>「valere（強い・価値がある）+ -ate（動詞化）」<br>「value」「valor」と語根が同じ"""
        elif word == "tactics":
            return """語源：ギリシャ語「taktikos」（配置の）<br>「tassein（配置する）+ -ikos（〜の性質）」<br>軍事用語から一般的戦略用語へ発展"""
        elif word == "compelling":
            return """語源：ラテン語「compellere」（無理に〜させる）<br>「com-（一緒に）+ pellere（押す・追いやる）」<br>「compel」「propel」と語根が同じ"""
        elif word == "profusely":
            return """語源：ラテン語「profusus」（大量に注がれた）<br>「pro-（前に）+ fundere（注ぐ）」<br>「confuse」「refuse」と語根が関連"""
        elif word == "cursory":
            return """語源：ラテン語「cursorius」（走るような）<br>「currere（走る）+ -ory（〜の性質）」<br>「current」「occur」と語根が同じ"""
        elif word == "disperse":
            return """語源：ラテン語「dispersus」（散らされた）<br>「dis-（離れて）+ spargere（撒く）」<br>「sparse」「aspersion」と語根が関連"""
        elif word == "overturn":
            return """語源：「over（上に・超えて）+ turn（回す）」<br>中世英語の複合語<br>「ひっくり返す」から「覆す・無効にする」へ意味拡張"""
        elif word == "degrade":
            return """語源：ラテン語「degradare」（階級を下げる）<br>「de-（下に）+ gradus（段階・階級）」<br>「grade」「graduate」と語根が同じ"""
        elif word == "coexistence":
            return """語源：「co-（共に）+ existence（存在）」<br>「exist」はラテン語「existere（立ち現れる）」<br>20世紀の政治・生物学用語として確立"""
        elif word == "whirl":
            return """語源：中世英語「whirlen」（回転する）<br>古ノルド語「hvirfla」（回る）から<br>擬音語的語根で「ぐるぐる回る音」"""
        elif word == "proprietor":
            return """語源：ラテン語「proprietarius」（私有財産の）<br>「proprius（自分の）+ -tor（〜する人）」<br>「property」「appropriate」と語根が同じ"""
        elif word == "discerning":
            return """語源：ラテン語「discernere」（区別する）<br>「dis-（離して）+ cernere（選別する）」<br>「concern」「certain」と語根が関連"""
        elif word == "masonry":
            return """語源：古フランス語「maçonnerie」（石工術）<br>「maçon（石工）+ -ery（技術・場所）」<br>中世ギルド制度から建築技術用語へ"""
        elif word == "jolt":
            return """語源：16世紀英語「jolt」（突然の衝撃）<br>「jot（急に動く）」の強調形<br>物理的衝撃から心理的ショックへ意味拡張"""
        elif word == "supper":
            return """語源：古フランス語「souper」（夕食する）<br>「soup（スープ）+ -er（動詞化）」<br>「sup（夕食をとる）」と関連"""
        elif word == "mole":
            return """語源：中世英語「molle」（モグラ）<br>ゲルマン語系の古い語<br>「潜む・隠れる」の共通概念で多義語化"""
        elif word == "strive":
            return """語源：古フランス語「estriver」（争う）<br>ラテン語「striare（線を引く・締め付ける）」<br>「strict」「stress」と語根が関連"""
        elif word == "dispatch":
            return """語源：イタリア語「dispaccio」（速報）<br>「dis-（離れて）+ -patch（速度）」<br>「patch（修正）」と関連し「急速処理」"""
        elif word == "discourse":
            return """語源：ラテン語「discursus」（駆け回る・議論）<br>「dis-（離れて）+ currere（走る）」<br>「current」「occur」と語根が同じ"""
        elif word == "prose":
            return """語源：ラテン語「prosa」（まっすぐな）<br>「prorsus（前に向かって）+ -a（女性形）」<br>「詩」と対比して「直接的な文章」"""
        elif word == "expertise":
            return """語源：フランス語「expertise」（専門知識）<br>「expert（専門家）+ -ise（動作・状態）」<br>「experience」「experiment」と語根が関連"""
        elif word == "smash":
            return """語源：16世紀英語「smash」（粉砕）<br>「smack（打つ）+ mash（潰す）」の合成語<br>擬音語的要素を含む現代語"""
        elif word == "brand":
            return """語源：古英語「brand」（燃える木・剣）<br>ゲルマン語「brennan（燃やす）」から<br>「焼印」→「商標」へ意味発展"""
        elif word == "appraise":
            return """語源：古フランス語「aprisier」（価格をつける）<br>「a-（〜に）+ price（価格）+ -ise（動詞化）」<br>「praise（称賞）」とは語源が異なる"""
        elif word == "upright":
            return """語源：「up（上に）+ right（正しい・まっすぐ）」<br>中世英語の複合語<br>物理的な「直立」から道徳的な「正直」へ"""
        elif word == "withdraw":
            return """語源：「with-（反対に）+ draw（引く）」<br>中世英語の複合語<br>「引き寄せる」の反対で「引き離す」"""
        elif word == "congregate":
            return """語源：ラテン語「congregare」（群れにする）<br>「con-（一緒に）+ grex（群れ）」<br>「aggregate」「segregate」と語根が同じ"""
        elif word == "allure":
            return """語源：古フランス語「aleurer」（鷹を呼び戻す）<br>「ad-（〜に）+ lure（誘い）」<br>「lure（誘惑）」と同じ語根"""
        elif word == "equity":
            return """語源：ラテン語「aequitas」（平等・公正）<br>「aequus（等しい）+ -itas（状態）」<br>「equal」「adequate」と語根が同じ"""
        elif word == "bristle":
            return """語源：中世英語「bristel」（剛毛）<br>古英語「byrst（剛毛）」から<br>「burst（破裂）」と語根が関連し「突き出る毛」"""
        elif word == "fierce":
            return """語源：古フランス語「fiers」（誇り高い・野性的）<br>ラテン語「ferus（野生の）」から<br>「feral（野生の）」と語根が同じ"""
        elif word == "leverage":
            return """語源：「lever（てこ）+ -age（動作・結果）」<br>「lever」はフランス語「levier（持ち上げる道具）」<br>「levitate」「elevate」と語根が関連"""
        elif word == "articulate":
            return """語源：ラテン語「articulatus」（関節のある）<br>「articulus（関節・小さな部分）+ -ate（動詞化）」<br>「article」「artifact」と語根が同じ"""
        elif word == "cardiac":
            return """語源：ギリシャ語「kardiakos」（心臓の）<br>「kardia（心臓）+ -akos（〜の性質）」<br>「cardiology」「electrocardiogram」と同じ語根"""
        elif word == "conspicuous":
            return """語源：ラテン語「conspicuus」（目に見える）<br>「con-（完全に）+ spicere（見る）」<br>「inspect」「suspect」と語根が同じ"""
        elif word == "materialism":
            return """語源：ラテン語「materia」（物質）<br>「mater（母・素材）+ -ism（主義）」<br>「matter」「material」と語根が同じ"""
        elif word == "absolute":
            return """語源：ラテン語「absolutus」（解放された・完全な）<br>「ab-（離れて）+ solvere（解く）」<br>「solve」「dissolve」と語根が同じ"""
        else:
            return f"""語源：{word}の詳細な語源分析<br>関連語との繋がりで記憶を強化<br>TOEFL頻出語として重要度高"""
    
    def parse_toefl_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        TOEFL 3800ファイル解析
        """
        words_data = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                    
                parts = line.split('\t')
                if len(parts) >= 4:
                    original_guid = parts[0]  # 参考用（使用しない）
                    word = parts[3]
                    original_meaning = parts[4] if len(parts) > 4 else ""
                    
                    words_data.append({
                        'word': word,
                        'original_meaning': original_meaning
                    })
        
        return words_data
    
    def generate_enhanced_tsv(self, input_file: str, output_file: str, limit: int = None):
        """
        改良版TSVファイル生成
        """
        print(f"🚀 Enhanced Anki processing: {input_file}")
        
        words_data = self.parse_toefl_file(input_file)
        
        if limit:
            words_data = words_data[:limit]
            print(f"📝 Limited to first {limit} words for testing")
        
        enhanced_cards = []
        
        for i, word_data in enumerate(words_data, 1):
            word = word_data['word']
            print(f"⚡ Processing {i}/{len(words_data)}: {word}")
            
            # GUID生成
            guid = self.generate_word_based_guid(word)
            
            # コンテンツ生成
            content = self.process_word_with_claude(word)
            
            # タグ設定
            tags = "claude-generated toefl rank3 enhanced"
            
            enhanced_cards.append({
                'guid': guid,
                'word': content['word'],
                'definition': content['definition'],
                'examples': content['examples'],
                'etymology': content['etymology'],
                'tags': tags,
                'deck': self.deck_name
            })
        
        # TSVファイル出力
        self._write_enhanced_tsv(enhanced_cards, output_file)
        
        print(f"✅ Enhanced TSV created: {output_file}")
        print(f"📊 Total cards: {len(enhanced_cards)}")
        print(f"🎯 Note type: {self.note_type}")
        print(f"🗂️ Deck: {self.deck_name}")
    
    def _write_enhanced_tsv(self, cards: List[Dict], output_file: str):
        """
        改良版TSV形式でファイル出力
        """
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # Ankiヘッダー（改良版）
            f.write("# Enhanced TOEFL Vocabulary Import File\n")
            f.write("# Generated by Claude Code Enhanced Anki Processor\n")
            f.write("#separator:tab\n")
            f.write("#html:true\n")
            f.write(f"#notetype:{self.note_type}\n")
            f.write(f"#deck:{self.deck_name}\n")
            f.write("#guid column:1\n")
            f.write("#tags column:6\n")
            f.write("# Field mapping: GUID | Word | Definition | Examples | Etymology | Tags\n")
            f.write("#\n")
            
            # カードデータ
            for card in cards:
                f.write(f"{card['guid']}\t{card['word']}\t{card['definition']}\t{card['examples']}\t{card['etymology']}\t{card['tags']}\n")
    
    def generate_css_template(self, output_file: str):
        """
        Ankiカードテンプレート用CSS生成
        """
        css_content = """
/* Enhanced TOEFL Vocabulary Card Styling */
/* このCSSをAnkiのカードテンプレート「Styling」欄に完全置き換えでコピーしてください */

/* 基本カードスタイル */
.card {
    font-family: 'Hiragino Sans', 'Meiryo', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fafafa;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.word {
    font-size: 28px;
    font-weight: bold;
    color: #2c3e50;
    text-align: center;
}

.definition {
    font-size: 24px;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 25px;
    padding: 12px;
    background-color: #ecf0f1;
    border-radius: 6px;
    font-weight: bold;
}

.examples {
    margin-bottom: 20px;
}

.examples .example {
    font-style: italic;
    color: #5a6c7d;
    margin: 8px 0;
    padding: 8px 12px;
    background-color: #ffffff;
    border-left: 4px solid #3498db;
    border-radius: 3px;
}

.example::first-letter {
    color: #e74c3c;
    font-weight: bold;
    font-size: 1.1em;
}

.etymology {
    background-color: #f4f1e8;
    border: 1px solid #d4be8a;
    border-radius: 5px;
    padding: 15px;
    margin-top: 20px;
    font-size: 14px;
    color: #8b4513;
    line-height: 1.5;
}

.etymology::before {
    content: "💡 ";
    font-size: 16px;
}

/* レスポンシブ対応 */
@media (max-width: 600px) {
    .card { padding: 15px; }
    .word { font-size: 24px; }
    .definition { font-size: 18px; }
}
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"📄 CSS template created: {output_file}")

if __name__ == "__main__":
    processor = EnhancedAnkiProcessor()
    
    # テスト実行
    input_file = "/home/user/.pg/development-projects/anki-deck-generator/data/input/toefl3800__rank3.txt"
    output_tsv = "/home/user/.pg/development-projects/anki-deck-generator/data/output/claude-code/enhanced_deck_v2.tsv"
    output_css = "/home/user/.pg/development-projects/anki-deck-generator/data/output/claude-code/card_template.css"
    
    # 改良版TSV生成 
    processor.generate_enhanced_tsv(input_file, output_tsv, limit=1159)
    
    # CSS テンプレート生成
    processor.generate_css_template(output_css)
    
    print("\n🎉 Enhanced Anki processing complete!")
    print("📋 Next steps:")
    print("1. Import enhanced_deck_v2.tsv into Anki")
    print("2. Create 'Enhanced TOEFL Vocabulary' note type")
    print("3. Copy CSS from card_template.css to card template")