import unittest
from unittest.mock import patch, MagicMock
from photos_and_videos_rename import listar_arquivos, obter_nome_novo_arquivo, retorna_novo_nome_arquivo_foto, retorna_novo_nome_arquivo_video


class TestFunctionsPhotosAndVideosRename(unittest.TestCase):

    @patch('photos_and_videos_rename.os.walk')
    @patch('photos_and_videos_rename.os.path.relpath')
    def test_listar_arquivos(self, mock_relpath, mock_walk):
        mock_relpath.side_effect = lambda x, y: x.replace(y, '').lstrip('\\/')
        mock_walk.return_value = [
            ('/pasta', [], ['arquivo.txt', 'imagem.jpg'])
        ]

        result = listar_arquivos('/pasta')
        self.assertEqual(result, ["arquivo.txt", "imagem.jpg"])

if __name__ == '__main__':
    unittest.main()
