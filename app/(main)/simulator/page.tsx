import { redirect } from "next/navigation";
import { FeedWrapper } from "@/components/feed-wrapper";
import { LanguageSelector } from "@/components/language-selector";
import { Promo } from "@/components/promo";
import { Quests } from "@/components/quests";
import { StickyWrapper } from "@/components/sticky-wrapper";
import { UserProgress } from "@/components/user-progress";
import {
    getCourseProgress,
    getCourses,
    getLessonPercentage,
    getUnits,
    getUserProgress,
    getUserSubscription,
} from "@/db/queries";

import { Header } from "../learn/header";
import { Unit } from "./unit";

const SimulatorPage = async () => {
    const userProgressData = getUserProgress();
    const courseProgressData = getCourseProgress();
    const lessonPercentageData = getLessonPercentage();
    const unitsData = getUnits();
    const userSubscriptionData = getUserSubscription();
    const coursesData = getCourses();

    const [
        userProgress,
        units,
        courseProgress,
        lessonPercentage,
        userSubscription,
        courses,
    ] = await Promise.all([
        userProgressData,
        unitsData,
        courseProgressData,
        lessonPercentageData,
        userSubscriptionData,
        coursesData,
    ]);

    if (!courseProgress || !userProgress || !userProgress.activeCourse)
        redirect("/courses");

    const isPro = !!userSubscription?.isActive;

    return (
        <div className="flex flex-row-reverse gap-[48px] px-6">
            <StickyWrapper>
                <UserProgress
                    activeCourse={userProgress.activeCourse}
                    hearts={userProgress.hearts}
                    points={userProgress.points}
                    hasActiveSubscription={isPro}
                />

                {!isPro && <Promo />}
                <Quests points={userProgress.points} />
            </StickyWrapper>
            <FeedWrapper>
                <Header title="Simulador">
                    <LanguageSelector
                        courses={courses}
                        activeCourseId={userProgress.activeCourse.id}
                    />
                </Header>
                {units.map((unit) => (
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
        </div>
    );
};

export default SimulatorPage;
