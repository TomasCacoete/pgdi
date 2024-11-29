import React from "react";

interface CompetitionItemProps {
    competition: any;
    handleSignUp: (competitionId: number) => void;
}

const CompetitionItem: React.FC<CompetitionItemProps> = ({ competition, handleSignUp }) => {
    return (
        <div className="competition-item">
            <h3>{competition.name}</h3>
            <p>
                <strong>Start:</strong> {new Date(competition.start_date).toLocaleString()}
            </p>
            <p>
                <strong>End:</strong> {new Date(competition.end_date).toLocaleString()}
            </p>
            <button onClick={() => handleSignUp(competition.id)}>
                Sign Up
            </button>
        </div>
    );
};

export default CompetitionItem;