
const url = "http://127.0.0.1:8000/api/appointments/appointments/";

const dataBase = [
    {"id": 101010, "ghl_id" : "abcde123", "location_id": 12345, "calendar_id": 123456, "contact_id": 99999}
];

async function Data() {
    try{
        const respuesta = await fetch(url);
        if(!respuesta.ok) throw new Error ("Error al llamr la Api 2.0");
        const dataress = await respuesta.json();
        return dataress;
    } catch (error){
        console.log(error)
        return dataBase;
    };  
}

export default Data;