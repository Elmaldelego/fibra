import { AudioPlayer } from "@/components/audio-player";
import { challengeOptions, challenges } from "@/db/schema";
import { cn } from "@/lib/utils";

import { Card } from "./card";

type ChallengeProps = {
  options: (typeof challengeOptions.$inferSelect)[];
  onSelect: (id: number) => void;
  status: "correct" | "wrong" | "none";
  selectedOption?: number;
  disabled?: boolean;
  type: (typeof challenges.$inferSelect)["type"];
  audioSrc?: string | null;
};

export const Challenge = ({
  options,
  onSelect,
  status,
  selectedOption,
  disabled,
  type,
  audioSrc,
}: ChallengeProps) => {
  return (
    <div
      className={cn(
        "grid gap-2",
        type === "ASSIST" && "grid-cols-1",
        type === "SELECT" &&
        "grid-cols-2 lg:grid-cols-[repeat(auto-fit,minmax(0,1fr))]",
        type === "LISTEN" && "grid-cols-1"
      )}
    >
      {type === "LISTEN" && audioSrc && (
        <div className="mb-8 w-full">
          <AudioPlayer src={audioSrc} />
        </div>
      )}
      {options.map((option, i) => (
        <Card
          key={option.id}
          id={option.id}
          text={option.text}
          imageSrc={option.imageSrc}
          shortcut={`${i + 1}`}
          selected={selectedOption === option.id}
          onClick={() => onSelect(option.id)}
          status={status}
          audioSrc={option.audioSrc}
          disabled={disabled}
          type={type}
        />
      ))}
    </div>
  );
};
