import unittest
from unittest.mock import Mock, patch
import json
from core.logic_engine import LogicEngine

class TestLogicEngine(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.engine = LogicEngine(api_key=self.api_key)
    
    @patch('openai.ChatCompletion.create')
    def test_extract_logic_success(self, mock_create):
        """测试成功提取逻辑"""
        # 模拟API响应
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content=json.dumps({
                "key_insights": ["测试洞察1", "测试洞察2"],
                "data_points": {"测试数据": "值"},
                "structure": "测试结构",
                "conclusions": ["测试结论1"],
                "recommendations": ["测试建议1"]
            })))
        ]
        mock_create.return_value = mock_response
        
        # 测试提取逻辑
        test_text = "这是测试文本，包含一些信息。"
        result = self.engine.extract_logic(test_text)
        
        # 验证结果
        self.assertIn("key_insights", result)
        self.assertIn("data_points", result)
        self.assertIn("structure", result)
        self.assertIn("conclusions", result)
        self.assertIn("recommendations", result)
    
    @patch('openai.ChatCompletion.create')
    def test_extract_logic_json_decode_error(self, mock_create):
        """测试JSON解析错误"""
        # 模拟API返回非JSON响应
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content="非JSON响应"))
        ]
        mock_create.return_value = mock_response
        
        # 测试异常
        test_text = "这是测试文本"
        with self.assertRaises(Exception) as context:
            self.engine.extract_logic(test_text)
        self.assertIn("不是有效的JSON", str(context.exception))
    
    @patch('openai.ChatCompletion.create')
    def test_extract_logic_timeout(self, mock_create):
        """测试API超时"""
        # 模拟API超时
        mock_create.side_effect = Exception("Timeout")
        
        # 测试异常
        test_text = "这是测试文本"
        with self.assertRaises(Exception) as context:
            self.engine.extract_logic(test_text)
        self.assertIn("API超时", str(context.exception))

if __name__ == '__main__':
    unittest.main()