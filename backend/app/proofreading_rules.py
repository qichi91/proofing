"""
校正ルールモジュール
textlintの代替として、日本語文書の校正チェックを行う
"""
import re
from typing import List, Dict


class ProofreadingRules:
    """校正ルールクラス"""
    
    def __init__(self):
        # 敬語の混在パターン
        self.dearu_patterns = [
            r'である[。、]',
            r'だ[。、]',
            r'〜た[。、]',
            r'〜る[。、]'
        ]
        
        self.desumasu_patterns = [
            r'です[。、]',
            r'ます[。、]',
            r'ました[。、]',
            r'ません[。、]'
        ]
        
        # 技術文書でよく使われる表記ゆれパターン
        self.notation_variations = {
            'サーバー': ['サーバ'],
            'コンピューター': ['コンピュータ'],
            'ユーザー': ['ユーザ'],
            'データベース': ['DB'],
            'アプリケーション': ['アプリ'],
            'インターフェース': ['インターフェイス', 'I/F'],
            'ファイル': ['file'],
            'システム': ['system'],
            'プロセス': ['process']
        }
        
        # 冗長表現パターン
        self.redundant_expressions = [
            r'することができます',
            r'することが可能です',
            r'〜することになります',
            r'〜していきます',
            r'まず最初に',
            r'一番最初',
            r'最も最適',
            r'より一層'
        ]
    
    def check_all_rules(self, text: str, filename: str = "") -> List[Dict]:
        """すべての校正ルールを適用してチェック"""
        issues = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            issues.extend(self.check_mixed_writing_style(line, line_num))
            issues.extend(self.check_notation_variations(line, line_num))
            issues.extend(self.check_redundant_expressions(line, line_num))
            issues.extend(self.check_doubled_particles(line, line_num))
            issues.extend(self.check_zero_width_spaces(line, line_num))
            issues.extend(self.check_successive_words(line, line_num))
            issues.extend(self.check_sentence_length(line, line_num))
            issues.extend(self.check_katakana_consistency(line, line_num))
        
        return issues
    
    def check_mixed_writing_style(self, text: str, line_num: int) -> List[Dict]:
        """「ですます調」と「である調」の混在をチェック"""
        issues = []
        
        has_dearu = any(re.search(pattern, text) for pattern in self.dearu_patterns)
        has_desumasu = any(re.search(pattern, text) for pattern in self.desumasu_patterns)
        
        if has_dearu and has_desumasu:
            issues.append({
                'type': 'mixed_writing_style',
                'severity': 'warning',
                'line': line_num,
                'message': '「ですます調」と「である調」が混在しています',
                'rule': 'no-mix-dearu-desumasu',
                'suggestion': '文体を統一してください'
            })
        
        return issues
    
    def check_notation_variations(self, text: str, line_num: int) -> List[Dict]:
        """表記ゆれをチェック"""
        issues = []
        
        for standard, variations in self.notation_variations.items():
            if standard in text:
                for variation in variations:
                    if variation in text and variation != standard:
                        issues.append({
                            'type': 'notation_variation',
                            'severity': 'info',
                            'line': line_num,
                            'message': f'表記ゆれの可能性があります: "{variation}" → "{standard}"',
                            'rule': 'notation-consistency',
                            'suggestion': f'"{standard}"に統一することを検討してください'
                        })
        
        return issues
    
    def check_redundant_expressions(self, text: str, line_num: int) -> List[Dict]:
        """冗長表現をチェック"""
        issues = []
        
        for pattern in self.redundant_expressions:
            if re.search(pattern, text):
                issues.append({
                    'type': 'redundant_expression',
                    'severity': 'info',
                    'line': line_num,
                    'message': f'冗長表現の可能性があります: {pattern}',
                    'rule': 'no-redundant-expression',
                    'suggestion': 'より簡潔な表現を検討してください'
                })
        
        return issues
    
    def check_doubled_particles(self, text: str, line_num: int) -> List[Dict]:
        """二重助詞をチェック"""
        issues = []
        particles = ['は', 'が', 'を', 'に', 'で', 'と', 'の', 'へ', 'から', 'まで']
        
        for particle in particles:
            # 連続する助詞をチェック
            pattern = f'{particle}[^{particle}]*{particle}'
            if re.search(pattern, text):
                issues.append({
                    'type': 'doubled_particle',
                    'severity': 'warning',
                    'line': line_num,
                    'message': f'助詞「{particle}」が重複している可能性があります',
                    'rule': 'no-doubled-joshi',
                    'suggestion': '文を分けるか、助詞を変更してください'
                })
        
        return issues
    
    def check_zero_width_spaces(self, text: str, line_num: int) -> List[Dict]:
        """ゼロ幅スペースをチェック"""
        issues = []
        zero_width_chars = ['\u200b', '\u200c', '\u200d', '\ufeff', '\u2060']
        
        for char in zero_width_chars:
            if char in text:
                issues.append({
                    'type': 'zero_width_space',
                    'severity': 'error',
                    'line': line_num,
                    'message': 'ゼロ幅スペースが検出されました',
                    'rule': 'no-zero-width-spaces',
                    'suggestion': 'ゼロ幅スペースを削除してください'
                })
        
        return issues
    
    def check_successive_words(self, text: str, line_num: int) -> List[Dict]:
        """連続する同一語句をチェック"""
        issues = []
        
        # 日本語の語句分割（簡易版）
        words = re.findall(r'[ぁ-んァ-ヶ一-龯]+', text)
        
        for i in range(len(words) - 1):
            if words[i] == words[i + 1] and len(words[i]) > 1:
                issues.append({
                    'type': 'successive_word',
                    'severity': 'warning',
                    'line': line_num,
                    'message': f'同一語句の連続使用が検出されました: 「{words[i]}」',
                    'rule': 'no-successive-word',
                    'suggestion': '表現を変更するか、語句を削除してください'
                })
        
        return issues
    
    def check_sentence_length(self, text: str, line_num: int, max_length: int = 120) -> List[Dict]:
        """文の長さをチェック"""
        issues = []
        
        sentences = re.split(r'[。！？]', text)
        for sentence in sentences:
            if len(sentence.strip()) > max_length:
                issues.append({
                    'type': 'long_sentence',
                    'severity': 'info',
                    'line': line_num,
                    'message': f'文が長すぎます（{len(sentence)}文字）',
                    'rule': 'max-sentence-length',
                    'suggestion': f'文を分割することを検討してください（推奨: {max_length}文字以下）'
                })
        
        return issues
    
    def check_katakana_consistency(self, text: str, line_num: int) -> List[Dict]:
        """カタカナ表記の一貫性をチェック"""
        issues = []
        
        # 長音記号の有無をチェック
        katakana_pairs = [
            ('コンピュータ', 'コンピューター'),
            ('サーバ', 'サーバー'),
            ('ユーザ', 'ユーザー'),
            ('データ', 'データー'),
            ('エラー', 'エラ'),
            ('フォルダ', 'フォルダー')
        ]
        
        for short_form, long_form in katakana_pairs:
            if short_form in text and long_form in text:
                issues.append({
                    'type': 'katakana_inconsistency',
                    'severity': 'info',
                    'line': line_num,
                    'message': f'カタカナ表記が統一されていません: 「{short_form}」と「{long_form}」',
                    'rule': 'katakana-consistency',
                    'suggestion': 'どちらか一方に統一してください'
                })
        
        return issues
