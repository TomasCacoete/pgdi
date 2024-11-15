import React, { useState } from "react";
import { GoogleMap, Marker, DirectionsRenderer, useLoadScript } from "@react-google-maps/api";

const MapsPage = () => {
   const { isLoaded } = useLoadScript({
       googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
   });

   const [origin, setOrigin] = useState(null);
   const [destination, setDestination] = useState(null);
   const [directions, setDirections] = useState(null);

   if (!isLoaded) return <div>Loading...</div>;

   const handleMapClick = (event) => {
       const { latLng } = event;

       if (!origin) {
           setOrigin({ lat: latLng.lat(), lng: latLng.lng() });
       } else if (!destination) {
           const dest = { lat: latLng.lat(), lng: latLng.lng() };
           setDestination(dest);
           calculateRoute(dest);
       }
   };

   const calculateRoute = (destinationPosition) => {
       const directionsService = new window.google.maps.DirectionsService();

       directionsService.route(
           {
               origin: origin,
               destination: destinationPosition,
               travelMode: window.google.maps.TravelMode.DRIVING,
           },
           (result, status) => {
               if (status === window.google.maps.DirectionsStatus.OK) {
                   setDirections(result);
               } else {
                   console.error("Error fetching directions", result);
               }
           }
       );
   };

   const resetRoute = () => {
       setOrigin(null);
       setDestination(null);
       setDirections(null);
   };

   return (
       <div style={{ height: "100vh", width: "100%" }}>
           <button onClick={resetRoute} style={{ position: "absolute", top: 10, left: 10, zIndex: 1 }}>
               Reset Route
           </button>

           <GoogleMap
               onClick={handleMapClick}
               center={{ lat: 40.748817, lng: -73.985428 }} // Default center (e.g., New York)
               zoom={12}
               mapContainerStyle={{ height: "100%", width: "100%" }}
           >
               {origin && <Marker position={origin} />}
               {destination && <Marker position={destination} />}
               {directions && <DirectionsRenderer directions={directions} />}
           </GoogleMap>
       </div>
   );
};

export default MapsPage;
