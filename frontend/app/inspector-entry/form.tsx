"use client";
import { createInspectorEntry } from "@/api/inspector";
import { ApiEntryItems, ApiVirtualCardModel } from "@/generated-client/Api";
import { Dispatch, SetStateAction } from "react";

const itemLabel: { [key in ApiEntryItems]: string } = {
  full_name: "名前",
  company_name: "会社名",
  position_name: "役職",
  email: "メールアドレス",
  address: "住所",
};

type Props = {
  virtualCard: ApiVirtualCardModel;
  inspectedItems: ApiEntryItems[];
  onSubmit: () => void;
  setVirtualCard: Dispatch<
    SetStateAction<ApiVirtualCardModel | null | undefined>
  >;
};

export default function Form(props: Props) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    props.setVirtualCard((prevCard) => {
      if (prevCard) {
        return {
          ...prevCard,
          entry: {
            ...prevCard.entry,
            [id]: value,
          },
        };
      }
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const { success } = await createInspectorEntry(props.virtualCard);
    if (success) {
      console.log("入力送信に成功しました");
      props.onSubmit();
    } else {
      alert("入力送信に失敗しました");
    }
  };

  return (
    <form className="w-full pr-4" onSubmit={handleSubmit}>
      <div className="flex flex-col">
        <div className="my-2 text-2xl">
          <span className="font-bold">ID:</span>
          <span className="font-normal">{props.virtualCard.id}</span>
        </div>
        <div className="my-2">
          {props.inspectedItems.map((item) => (
            <div className="form-group py-2 first:pb-2 last:pt-2" key={item}>
              <label htmlFor={item}>{itemLabel[item]}</label>
              <input
                id={item}
                type="text"
                className="form-control"
                data-1p-ignore
                value={props.virtualCard.entry[item]}
                onChange={handleChange}
              />
            </div>
          ))}
        </div>
        <div className="flex my-2 justify-end">
          <button type="submit" className="btn btn-primary w-16">
            送信
          </button>
        </div>
      </div>
    </form>
  );
}
