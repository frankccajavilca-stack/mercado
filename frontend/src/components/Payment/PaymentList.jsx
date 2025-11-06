
import { useEffect, useState } from "react";
import Data from "../../services/payList";

export default function PaymentList() {
    const [datos, setDatos] = useState([]);
    const [loading, setLoading] = useState(true); // inicia en true

    useEffect(() => {
        const fetchData = async () => {
            try {
                const ress = await Data();
                setDatos(ress);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false); // ya terminó de cargar
            }
        };

        fetchData();
    }, []); // <-- arreglo vacío para que se ejecute solo una vez al montar

    if (loading) return <p>Cargando ...</p>;

    return (
        <div className="card">
            <table>
                <thead>
                    <tr>
                        <th>ghl_id</th>
                        <th>location_id</th>
                        <th>calendar_id</th>
                        <th>contact_id</th>
                    </tr>
                </thead>
                <tbody>
                    {datos.map((item) => (
                        <tr key={item.id}>
                            <td>{item.ghl_id}</td>
                            <td>{item.location_id}</td>
                            <td>{item.calendar_id}</td>
                            <td>{item.contact_id}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
// {item.ghl_id} - {item.location_id} - {item.calendar_id} - {item.contact_id}