"use client";

import { useState } from "react";

import { FeedWrapper } from "@/components/feed-wrapper";
import { UnitSelector } from "@/components/unit-selector";

import { Header } from "./header";
import { Unit } from "./unit";

type Lesson = {
    id: number;
    title: string;
    unitId: number;
    order: number;
    completed: boolean;
    challenges: {
        id: number;
        lessonId: number;
        type: "SELECT" | "ASSIST" | "LISTEN";
        question: string;
        order: number;
        challengeProgress: {
            id: number;
            userId: string;
            challengeId: number;
            completed: boolean;
        }[];
    }[];
};

type UnitType = {
    id: number;
    title: string;
    description: string;
    courseId: number;
    order: number;
    lessons: Lesson[];
};

type CourseProgress = {
    activeLesson?: {
        id: number;
        title: string;
        unitId: number;
        order: number;
        unit: {
            id: number;
            title: string;
            description: string;
            courseId: number;
            order: number;
        };
        challenges: {
            id: number;
            lessonId: number;
            type: "SELECT" | "ASSIST" | "LISTEN";
            question: string;
            order: number;
            challengeProgress: {
                id: number;
                userId: string;
                challengeId: number;
                completed: boolean;
            }[];
        }[];
    };
    activeLessonId?: number;
};

type Props = {
    courseTitle: string;
    units: UnitType[];
    courseProgress: CourseProgress;
    lessonPercentage: number;
};

export const LearnContent = ({
    courseTitle,
    units,
    courseProgress,
    lessonPercentage,
}: Props) => {
    const [selectedUnitId, setSelectedUnitId] = useState<number | null>(null);

    // Filter units based on selection
    const displayedUnits = selectedUnitId
        ? units.filter((unit: UnitType) => unit.id === selectedUnitId)
        : units;

    return (
        <FeedWrapper>
            <Header title={courseTitle}>
                <UnitSelector
                    units={units.map((u: UnitType) => ({
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
