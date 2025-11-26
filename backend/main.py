"""Simplified FastAPI application for DogDietApp.
Uses synchronous psycopg2 access without async pools or external schema/service modules.
"""

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from database import insert_dog_questionnaire, get_db_connection
from Report_select import choose_report

app = FastAPI(title="Dog Diet API", description="API for dog diet recommendations and breed management", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DogQuestionnaireInput(BaseModel):
    breed_name_AKC: str = Field(..., description="Official AKC breed name")
    age_years_preReg: float = Field(..., ge=0, le=30, description="Dog's age in years")
    status_dietRelat_preReg: List[str] = Field(..., description="List of diet-related health statuses")


class BreedCreateInput(BaseModel):
    breed_name_AKC: str
    breed_otherNames: Optional[str] = None
    breed_group_AKC: Optional[str] = None
    breed_size_categ_AKC: Optional[str] = None
    breed_life_expect_yrs: Optional[float] = None
    food_recomm_brand: Optional[str] = None
    food_recomm_product: Optional[str] = None
    food_recomm_format: Optional[str] = None
    listed_DogDiet_MVP: Optional[str] = None
    dogapi_id: Optional[str] = None


class BreedUpdateInput(BaseModel):
    breed_otherNames: Optional[str] = None
    breed_group_AKC: Optional[str] = None
    breed_size_categ_AKC: Optional[str] = None
    breed_life_expect_yrs: Optional[float] = None
    food_recomm_brand: Optional[str] = None
    food_recomm_product: Optional[str] = None
    food_recomm_format: Optional[str] = None
    listed_DogDiet_MVP: Optional[str] = None


class BreedFullUpdateInput(BaseModel):
    breed_name_AKC: str
    breed_group_AKC: str
    breed_size_categ_AKC: str
    breed_otherNames: Optional[str] = None
    breed_life_expect_yrs: Optional[float] = None
    food_recomm_brand: Optional[str] = None
    food_recomm_product: Optional[str] = None
    food_recomm_format: Optional[str] = None
    listed_DogDiet_MVP: Optional[str] = None
    dogapi_id: Optional[str] = None


@app.get("/api/breeds")
def get_all_breeds():
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT breed_name_AKC, breed_group_AKC, breed_size_categ_AKC FROM breeds_AKC_Rsrch_FoodV1 ORDER BY breed_name_AKC")
        rows = cur.fetchall()
        cur.close(); conn.close()
        breeds = [
            {
                'breed_name_AKC': r[0],
                'breed_group_AKC': r[1],
                'breed_size_categ_AKC': r[2]
            } for r in rows
        ]
        return {'success': True, 'message': 'Retrieved all breeds', 'breeds': breeds}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/breed/{search_field}/{search_value}")
def get_breed(
    search_field: str = Path(..., description="Search by 'breed_name_AKC' or 'dogapi_id'"),
    search_value: str = Path(..., description="The breed name or ID to search for")
):
    if search_field not in ['breed_name_AKC', 'dogapi_id']:
        raise HTTPException(status_code=400, detail='Invalid search field. Use breed_name_AKC or dogapi_id')
    try:
        conn = get_db_connection(); cur = conn.cursor()
        if search_field == 'breed_name_AKC':
            cur.execute("SELECT * FROM breeds_AKC_Rsrch_FoodV1 WHERE breed_name_AKC=%s", (search_value,))
        else:
            cur.execute("SELECT * FROM breeds_AKC_Rsrch_FoodV1 WHERE dogapi_id=%s", (search_value,))
        row = cur.fetchone(); cur.close(); conn.close()
        if not row:
            raise HTTPException(status_code=404, detail='Breed not found')
        columns = [
            'breed_name_AKC','breed_otherNames','breed_group_AKC','breed_size_categ_AKC','breed_life_expect_yrs',
            'listed_DogDiet_MVP','food_recomm_brand','food_recomm_product','food_recomm_format','food_rec_note_INTERNAL',
            'size_category','breed_class_AKC','dogapi_id'
        ]
        breed = {col: row[i] for i, col in enumerate(columns) if i < len(row)}
        return {'success': True, 'message': f'Retrieved breed by {search_field}', 'breed': breed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/submit-dog-info")
def submit_dog_info(data: DogQuestionnaireInput):
    try:
        breed_name = data.breed_name_AKC
        age_years = data.age_years_preReg
        status_list = data.status_dietRelat_preReg
        db_result = insert_dog_questionnaire(breed_name, age_years, status_list)
        report_message = choose_report(status_list, breed_name)
        return {
            'success': True,
            'message': 'Dog information submitted successfully!',
            'record_id': db_result['id'],
            'report': report_message,
            'breed': breed_name,
            'age': age_years,
            'statuses': status_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/breed/{search_field}/{search_value}")
def update_breed_partial(
    search_field: str = Path(..., description="Search by 'breed_name_AKC' or 'dogapi_id'"),
    search_value: str = Path(..., description="The breed name or ID to update"),
    data: BreedUpdateInput = None
):
    if search_field not in ['breed_name_AKC', 'dogapi_id']:
        raise HTTPException(status_code=400, detail='Invalid search field. Use breed_name_AKC or dogapi_id')
    update_data = data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail='No update data provided')
    try:
        assignments = ', '.join([f"{field}=%s" for field in update_data.keys()])
        values = list(update_data.values())
        conn = get_db_connection(); cur = conn.cursor()
        if search_field == 'breed_name_AKC':
            cur.execute(f"UPDATE breeds_AKC_Rsrch_FoodV1 SET {assignments} WHERE breed_name_AKC=%s", values + [search_value])
        else:
            cur.execute(f"UPDATE breeds_AKC_Rsrch_FoodV1 SET {assignments} WHERE dogapi_id=%s", values + [search_value])
        conn.commit(); cur.close(); conn.close()
        return {
            'success': True,
            'message': f'Breed updated successfully via {search_field}',
            'updated_fields': list(update_data.keys()),
            'search_value': search_value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/breed/{search_field}/{search_value}")
def update_breed_full(
    search_field: str = Path(..., description="Search by 'breed_name_AKC' or 'dogapi_id'"),
    search_value: str = Path(..., description="The breed name or ID to update"),
    data: BreedFullUpdateInput = None
):
    if search_field not in ['breed_name_AKC', 'dogapi_id']:
        raise HTTPException(status_code=400, detail='Invalid search field. Use breed_name_AKC or dogapi_id')
    try:
        conn = get_db_connection(); cur = conn.cursor()
        if search_field == 'breed_name_AKC':
            cur.execute("UPDATE breeds_AKC_Rsrch_FoodV1 SET breed_group_AKC=%s, breed_size_categ_AKC=%s WHERE breed_name_AKC=%s",
                        (data.breed_group_AKC, data.breed_size_categ_AKC, search_value))
        else:
            cur.execute("UPDATE breeds_AKC_Rsrch_FoodV1 SET breed_group_AKC=%s, breed_size_categ_AKC=%s WHERE dogapi_id=%s",
                        (data.breed_group_AKC, data.breed_size_categ_AKC, search_value))
        conn.commit(); cur.close(); conn.close()
        return {'success': True, 'message': f'Breed fully replaced successfully via {search_field}', 'search_value': search_value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/breed/{search_field}/{search_value}")
def delete_breed(
    search_field: str = Path(..., description="Search by 'breed_name_AKC' or 'dogapi_id'"),
    search_value: str = Path(..., description="The breed name or ID to delete")
):
    if search_field not in ['breed_name_AKC', 'dogapi_id']:
        raise HTTPException(status_code=400, detail='Invalid search field. Use breed_name_AKC or dogapi_id')
    try:
        conn = get_db_connection(); cur = conn.cursor()
        if search_field == 'breed_name_AKC':
            cur.execute("DELETE FROM breeds_AKC_Rsrch_FoodV1 WHERE breed_name_AKC=%s", (search_value,))
        else:
            cur.execute("DELETE FROM breeds_AKC_Rsrch_FoodV1 WHERE dogapi_id=%s", (search_value,))
        conn.commit(); cur.close(); conn.close()
        return {'success': True, 'message': 'Breed deleted successfully', 'deleted': search_value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
