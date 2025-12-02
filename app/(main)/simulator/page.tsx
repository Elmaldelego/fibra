import { redirect } from "next/navigation";

import { Promo } from "@/components/promo";
import { Quests } from "@/components/quests";
import { StickyWrapper } from "@/components/sticky-wrapper";
import { UserProgress } from "@/components/user-progress";
import {
    getExams,
    getUserProgress,
    getUserSubscription,
} from "@/db/queries";

import { SimulatorContent } from "./simulator-content";

const SimulatorPage = async () => {
    const userProgressData = getUserProgress();
    const examsData = getExams();
    const userSubscriptionData = getUserSubscription();

    const [
        userProgress,
        exams,
        userSubscription,
    ] = await Promise.all([
        userProgressData,
        examsData,
        userSubscriptionData,
    ]);

    if (!userProgress || !userProgress.activeCourse)
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
            <SimulatorContent
                exams={exams}
            />
        </div>
    );
};

export default SimulatorPage;

