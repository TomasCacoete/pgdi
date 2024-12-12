import Footer from "../../components/Footer/Footers";

import "./LandingPage.scss";

import LogoWhite from "../../assets/logo-white.svg";
import PhoneApp from "../../assets/phone-app.png";

export default function LandingPage(){
    return(
        <>
            <div className="landing">
                <div className="info">
                    <img src={LogoWhite}/>

                    <h1>
                        Ride, Compete, and<br/>
                        Give Back
                    </h1>

                    <h3>
                        JOIN TourDash for flexible cycling<br/>
                        challenges and meaningful impact
                    </h3>

                    <button>
                        Join Now
                    </button>
                </div>

                <img src={PhoneApp}/>
                
            </div>
            
            <Footer/>
        </>
    );
};