from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client
from django.conf import settings


@deconstructible
class FDFSStorage(Storage):
    """fast dfs文件存储类"""
    def __init__(self, client_conf=None, base_url=None):
        """初始化"""
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF

        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL

        self.base_url = base_url

    def _open(self, name, mode='rb'):
        """打开文件时使用"""
        pass

    def _save(self, name, content):
        """保存文件时使用"""
        # name：你选择上传文件的名字
        # content：包含你上传文件内容的file对象
        
        # 创建 Fdfs_client 对象
        cilent = Fdfs_client(self.client_conf)

        # 上传文件到 fast dfs 存储系统中
        res = cilent.upload_by_buffer(content.read())
        """
        dict {
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,
            'Status'          : 'Upload successed.',
            'Local file name' : '',
            'Uploaded size'   : upload_size,
            'Storage IP'      : storage_ip
        }
        """
        if res.get('Status') != 'Upload successed.':
            """上传失败"""
            raise Exception("上传文件到fast dfs失败")

        # 获取返回的文件ID
        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        """Django判断上传文件名是否可用"""
        # 如果提供的名称所引用的文件在文件系统中存在，则返回True，否则如果这个名称可用于新文件，则返回False
        # 因为文件存储到Fast dfs系统上了，所以永远不会因为重名而出错，我们可以直接返回False
        return False

    def url(self, name):
        """返回访问文件的url路径"""
        return self.base_url+name

