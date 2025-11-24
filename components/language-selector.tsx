"use client";

import { useTransition } from "react";

import { ChevronDown, Loader } from "lucide-react";
import Image from "next/image";

import { upsertUserProgress } from "@/actions/user-progress";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { courses } from "@/db/schema";

type Props = {
    courses: (typeof courses.$inferSelect)[];
    activeCourseId: number;
};

export const LanguageSelector = ({ courses, activeCourseId }: Props) => {
    const [pending, startTransition] = useTransition();

    const activeCourse = courses.find((c) => c.id === activeCourseId);

    const onSelect = (id: number) => {
        if (id === activeCourseId) return;

        startTransition(() => {
            upsertUserProgress(id).catch(() => { });
        });
    };

    if (!activeCourse) return null;

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="w-full justify-between" size="lg">
                    <div className="flex items-center gap-x-2">
                        <Image
                            src={activeCourse.imageSrc}
                            alt={activeCourse.title}
                            height={32}
                            width={32}
                            className="rounded-md border"
                        />
                        <span className="font-bold text-neutral-700">
                            {activeCourse.title}
                        </span>
                    </div>
                    <ChevronDown className="h-4 w-4 text-neutral-500 opacity-50" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-[200px]">
                {courses.map((course) => (
                    <DropdownMenuItem
                        key={course.id}
                        onClick={() => onSelect(course.id)}
                        className="cursor-pointer"
                        disabled={pending}
                    >
                        <div className="flex items-center gap-x-2 w-full">
                            <Image
                                src={course.imageSrc}
                                alt={course.title}
                                height={24}
                                width={24}
                                className="rounded-md border"
                            />
                            <span className="font-bold text-neutral-700">{course.title}</span>
                            {pending && course.id === activeCourseId && (
                                <Loader className="h-4 w-4 animate-spin ml-auto" />
                            )}
                        </div>
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
};
