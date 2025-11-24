"use client";

import { useAudio } from "react-use";

type AudioPlayerProps = {
    src: string;
};

export const AudioPlayer = ({ src }: AudioPlayerProps) => {
    const [audio, state, controls] = useAudio({
        src,
        autoPlay: false,
    });

    return (
        <div className="flex w-full flex-col items-center justify-center gap-y-4 rounded-xl border-2 bg-slate-100 p-4">
            {audio}
            <div className="flex w-full items-center justify-center gap-x-4">
                <button
                    onClick={state.playing ? controls.pause : controls.play}
                    className="rounded-full bg-sky-500 p-3 text-white transition hover:bg-sky-600"
                >
                    {state.playing ? (
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            strokeWidth={1.5}
                            stroke="currentColor"
                            className="h-6 w-6"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="M15.75 5.25v13.5m-7.5-13.5v13.5"
                            />
                        </svg>
                    ) : (
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            strokeWidth={1.5}
                            stroke="currentColor"
                            className="h-6 w-6"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.348a1.125 1.125 0 010 1.971l-11.54 6.347a1.125 1.125 0 01-1.667-.985V5.653z"
                            />
                        </svg>
                    )}
                </button>
            </div>
        </div>
    );
};
