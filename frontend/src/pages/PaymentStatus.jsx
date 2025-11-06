
import { useEffect, useState } from "react"
import Uzi from "../services/uzi"

export default function PaymentStatus(){
    
    const [totalescitas , setTotalescitas] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const obtenerDatos = async () => {
            try{
                const datos = await Uzi();
                setTotalescitas(datos.length);
            } catch(error){
                console.error(error)
            } finally{
                setLoading(false)
            }
        };
        obtenerDatos();
    }, []);

    if (loading) return <p>cargando ...</p> 

    return(
        <div className="card">
            <h1>{totalescitas} citas en la Lista</h1>
        </div>
    );

}