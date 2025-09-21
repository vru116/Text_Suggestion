from typing import List

class PrefixTreeNode:
    def __init__(self):
        self.children: dict[str, PrefixTreeNode] = {}
        self.is_end_of_word = False

class PrefixTree:
    def __init__(self, vocabulary: List[str]):
        """
        vocabulary: список всех уникальных токенов в корпусе
        """
        self.root = PrefixTreeNode()
        
        for word in vocabulary:
            cur_node = self.root

            for sym in word:
                if not (sym in cur_node.children):
                    cur_node.children[sym] = PrefixTreeNode()
                cur_node = cur_node.children[sym]
            cur_node.is_end_of_word = True

    def find_node_by_prefix(self, prefix):
        cur_node = self.root
        for sym in prefix:
            if sym not in cur_node.children:
                return None
            cur_node = cur_node.children[sym]
        return cur_node
    
    def dfs(self, node, prefix, result):
        if node.is_end_of_word:
            result.append(prefix)
        for sym, child in node.children.items():
            self.dfs(child, prefix + sym, result)
        
        return result


    def search_prefix(self, prefix) -> List[str]:
        """
        Возвращает все слова, начинающиеся на prefix
        prefix: str – префикс слова
        """
        prefix_node = self.find_node_by_prefix(prefix)
        if prefix_node is None:
            return []
        return self.dfs(prefix_node, prefix, [])
    

class WordCompletor:
    def __init__(self, corpus):
        """
        corpus: list – корпус текстов
        """
        
        self.word_probs = {}
        vocabulary = []
        self.total_words = 0

        for text in corpus:
            for word in text:
                self.total_words += 1
                if word not in self.word_probs:
                    self.word_probs[word] = 0
                    vocabulary.append(word)
                self.word_probs[word] += 1

        for word in self.word_probs:
            self.word_probs[word] /= self.total_words

        self.prefix_tree = PrefixTree(vocabulary=vocabulary)

    def get_words_and_probs(self, prefix: str) -> (List[str], List[float]):
        """
        Возвращает список слов, начинающихся на prefix,
        с их вероятностями (нормировать ничего не нужно)
        """
        words, probs = [], []
        
        words = self.prefix_tree.search_prefix(prefix)
        probs = []
        for word in words:
            probs.append(self.word_probs[word])
        return words, probs