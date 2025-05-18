import os

import pythoncom
import win32com
from loguru import logger


class CATIAOperator:
    def __init__(self):
        pythoncom.CoInitialize()
        self.catia = None
        self.part = None
        self._connect()

    def __del__(self):
        if self.catia:
            self.catia.Quit()
        pythoncom.CoUninitialize()

    def _connect(self):
        try:
            self.catia = win32com.client.Dispatch('CATIA.Application')
            self.catia.Visible = True
            logger.info("已连接到运行中的CATIA实例")
        except Exception as e:
            logger.critical(f"无法连接CATIA: {str(e)}")
            raise

    def open_document(self, file_path: str):
        try:
            if not self.catia:
                self._connect()
            document = self.catia.Documents.Open(file_path)
            self.catia.Visible = True
            self.part = document.Part
            if not self.part:
                raise ValueError("无法获取活动文档的 Part 对象")
            logger.info(f"成功打开文件: {file_path}")
        except Exception as e:
            logger.error(f"打开文件失败: {str(e)}")
            raise
    def export_to_stp(self, file_path: str):
        """
        将当前打开的CATIA模型导出为STP格式。

        Args:
        file_path: 导出文件的完整路径，包括文件名和.STP扩展名。

        Returns:
        None
        """
        try:
            if not self.part:
                raise ValueError("未打开CATPart文件，无法导出")

            # 检查文件路径
            if not file_path:
                raise ValueError("导出路径不能为空")

            # 获取保存目录
            save_dir = os.path.dirname(file_path)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # 检查文件扩展名
            if not file_path.lower().endswith(".stp"):
                file_path += ".stp"

            # 获取活动文档
            active_document = self.catia.ActiveDocument

            # 尝试导出模型到STP文件
            try:
                active_document.ExportData(file_path, "STEP")
                logger.info(f"模型已成功导出为STP格式，保存路径：{file_path}")
            except Exception as e:
                raise Exception(f"导出到STP时发生错误: {str(e)}")

        except Exception as e:
            logger.error(f"导出到STP时发生错误: {str(e)}")
            raise
    def set_dimensions(self, length: float = None, width: float = None, height: float = None):
        try:
            if not self.catia:
                raise ValueError("CATIA 应用程序未初始化")
            if not self.part:
                raise ValueError("未打开CATPart文件")

            parameters = self.part.Parameters
            for param in parameters:
                if param.Name == "长" and length is not None:
                    param.Value = length
                elif param.Name == "宽" and width is not None:
                    param.Value = width
                elif param.Name == "高" and height is not None:
                    param.Value = height

            self.part.Update()
            return {
                "length": length if length is not None else self.get_current_dimension("长"),
                "width": width if width is not None else self.get_current_dimension("宽"),
                "height": height if height is not None else self.get_current_dimension("高")
            }
        except Exception as e:
            logger.error(f"更新长宽高参数失败: {str(e)}")
            raise

    def get_current_dimension(self, dimension_name: str):
        try:
            if not self.part:
                raise ValueError("未打开CATPart文件")
            parameters = self.part.Parameters
            for param in parameters:
                if param.Name == dimension_name:
                    return param.Value
            logger.error(f"无法找到参数: {dimension_name}")
            raise ValueError(f"无法找到参数: {dimension_name}")
        except Exception as e:
            logger.error(f"获取参数值失败: {str(e)}")
            raise