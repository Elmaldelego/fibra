"use client";

import { useState } from "react";

import { FeedWrapper } from "@/components/feed-wrapper";
import { UnitSelector } from "@/components/unit-selector";

import { Header } from "../learn/header";
import { Unit } from "./unit";

type Props = {
    units: any[];
    courseProgress: any;
    lessonPercentage: number;
};

export const SimulatorContent = ({
    units,
    courseProgress,
    lessonPercentage,
}: Props) => {
    const [selectedUnitId, setSelectedUnitId] = useState<number | null>(null);

    // Filter units based on selection
    const displayedUnits = selectedUnitId
        ? units.filter((unit) => unit.id === selectedUnitId)
        : units;

    return (
        <FeedWrapper>
            <Header title="Simulador">
                <UnitSelector
                    units={units.map((u) => ({
                        id: u.id,
                        title: u.title,
                        description: u.description,
                        order: u.order,
                    }))}
                    selectedUnitId={selectedUnitId}
                    onSelectUnit={setSelectedUnitId}
                />
            </Header>
            {displayedUnits.map((unit) => (
                <div key={unit.id} className="mb-10">
                    <Unit
                        id={unit.id}
                        order={unit.order}
                        description={unit.description}
                        title={unit.title}
                        lessons={unit.lessons}
                        activeLesson={courseProgress.activeLesson}
                        activeLessonPercentage={lessonPercentage}
                    />
                </div>
            ))}
        </FeedWrapper>
    );
};
