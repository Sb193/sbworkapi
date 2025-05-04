from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class SortField(str, Enum):
    CREATED_AT = "created_at"
    SALARY_MIN = "salary_min"
    SALARY_MAX = "salary_max"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class JobSearchQuery(BaseModel):
    q: Optional[str] = Field(None, description="Từ khóa tìm kiếm")
    location_id: Optional[int] = Field(None, description="ID địa điểm")
    work_type_id: Optional[int] = Field(None, description="ID loại hình công việc")
    experience_level: Optional[str] = Field(None, description="Mức kinh nghiệm")
    industry: Optional[str] = Field(None, description="Ngành nghề")
    tag_ids: Optional[List[int]] = Field(None, description="Danh sách ID tags")
    salary_min: Optional[int] = Field(None, description="Mức lương tối thiểu")
    salary_max: Optional[int] = Field(None, description="Mức lương tối đa")
    page: int = Field(1, ge=1, description="Số trang")
    per_page: int = Field(10, ge=1, le=100, description="Số bản ghi mỗi trang")
    sort: Optional[SortField] = Field(SortField.CREATED_AT, description="Trường sắp xếp")
    order: Optional[SortOrder] = Field(SortOrder.DESC, description="Thứ tự sắp xếp")

class JobSearchResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    per_page: int
    total_pages: int 