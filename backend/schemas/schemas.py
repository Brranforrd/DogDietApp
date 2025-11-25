# backend/schemas/schemas.py - Pydantic models for API request/response validation

from pydantic import BaseModel, Field  # Import Pydantic for data validation models
from typing import List, Optional  # Import type hints for better code clarity


# ==================== Request/Response Schemas ====================

class DogQuestionnaireInput(BaseModel):
    """
    Data model for user dog questionnaire submissions.
    Used in POST /api/submit-dog-info endpoint.
    """
    breed_name_AKC: str = Field(
        ...,  # ... means required field
        description="Official AKC breed name",
        example="Labrador Retriever"
    )
    age_years_preReg: float = Field(
        ...,
        ge=0,  # ge = greater than or equal to
        le=30,  # le = less than or equal to
        description="Dog's age in years (can include decimal for months)",
        example=3.5
    )
    status_dietRelat_preReg: List[str] = Field(
        ...,
        description="List of diet-related health statuses",
        example=["none"]
    )


class BreedCreateInput(BaseModel):
    """
    Data model for creating new breed records.
    Used in POST /api/breed endpoint.
    """
    breed_name_AKC: str = Field(..., description="Official AKC breed name")
    breed_otherNames: Optional[str] = Field(
        None,  # Optional field with None as default
        description="Other names for this breed, separated by semicolons"
    )
    breed_group_AKC: Optional[str] = Field(
        None,
        description="AKC breed group (sporting, hound, working, etc.)"
    )
    breed_size_categ_AKC: Optional[str] = Field(
        None,
        description="Size category: small, medium, large, or extra large"
    )
    breed_life_expect_yrs: Optional[float] = Field(
        None,
        ge=0,
        le=30,
        description="Average life expectancy in years"
    )
    food_recomm_brand: Optional[str] = Field(
        None,
        description="Recommended dog food brand"
    )
    food_recomm_product: Optional[str] = Field(
        None,
        description="Specific recommended product name"
    )
    food_recomm_format: Optional[str] = Field(
        None,
        description="Food format: kibble, wet, raw, etc."
    )
    listed_DogDiet_MVP: Optional[str] = Field(
        None,
        description="Y or N - whether included in MVP version",
        max_length=1
    )
    dogapi_id: Optional[str] = Field(
        None,
        description="35-character ID from DogAPI.org"
    )


class BreedUpdateInput(BaseModel):
    """
    Data model for partial breed updates (PATCH).
    All fields are optional - only provided fields will be updated.
    Used in PATCH /api/breed/{search_field}/{search_value} endpoint.
    """
    breed_otherNames: Optional[str] = None
    breed_group_AKC: Optional[str] = None
    breed_size_categ_AKC: Optional[str] = None
    breed_life_expect_yrs: Optional[float] = Field(None, ge=0, le=30)
    food_recomm_brand: Optional[str] = None
    food_recomm_product: Optional[str] = None
    food_recomm_format: Optional[str] = None
    listed_DogDiet_MVP: Optional[str] = Field(None, max_length=1)


class BreedFullUpdateInput(BaseModel):
    """
    Data model for full breed replacement (PUT).
    Required fields must be present - replaces entire record.
    Used in PUT /api/breed/{search_field}/{search_value} endpoint.
    """
    # Required fields for full update
    breed_name_AKC: str = Field(..., description="Official AKC breed name")
    breed_group_AKC: str = Field(..., description="AKC breed group")
    breed_size_categ_AKC: str = Field(..., description="Size category")
    
    # Optional fields
    breed_otherNames: Optional[str] = None
    breed_life_expect_yrs: Optional[float] = Field(None, ge=0, le=30)
    food_recomm_brand: Optional[str] = None
    food_recomm_product: Optional[str] = None
    food_recomm_format: Optional[str] = None
    listed_DogDiet_MVP: Optional[str] = Field(None, max_length=1)
    dogapi_id: Optional[str] = None


# ==================== Response Schemas (Optional but Recommended) ====================

class BreedResponse(BaseModel):
    """
    Data model for breed data returned from database.
    Used in GET endpoints for consistent response structure.
    """
    breed_name_AKC: str
    breed_group_AKC: Optional[str] = None
    breed_life_expect_yrs: Optional[float] = None
    listed_DogDiet_MVP: Optional[str] = None
    food_recomm_product: Optional[str] = None
    dogapi_id: Optional[str] = None


class QuestionnaireResponse(BaseModel):
    """
    Data model for successful questionnaire submission response.
    """
    success: bool
    message: str
    report: str
    breed: str
    age: float
    statuses: List[str]


class StandardResponse(BaseModel):
    """
    Generic success/error response model.
    """
    success: bool
    message: str
