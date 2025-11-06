" yooooo Edwin "


const url = "http://127.0.0.1:8000/api/appointments/appointments/";

async function Uzi() {
    try{
        const respuesta = await fetch(url);
        if(!respuesta.ok) throw new Error ("Error al llamar la Api 2.0");
        const dataress = await respuesta.json();
        return dataress;
    } catch (error){
        console.log(error)
        return "Error al llamar Api"
    };  
}

export default Uzi;