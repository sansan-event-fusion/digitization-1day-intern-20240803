"use client";

import {
  ApiEntryItems,
  ApiInspectedVirtualCardModel,
  ApiVirtualCardModel,
} from "@/generated-client/Api";
import Form from "./form";
import Image from "next/image";
import { newInspectEntry } from "@/api/inspector";
import { useEffect, useState } from "react";

export default function EntryPanel() {
  const [virtualCard, setVirtualCard] = useState<
    ApiVirtualCardModel | null | undefined
  >(null);
  const [inspectedItems, setInspectedItems] = useState<ApiEntryItems[]>([]);
  const [imagePath, setImagePath] = useState<string>("");

  const fetchEntry = async () => {
    const { success, data } = await newInspectEntry();
    if (success) {
      const { id, entry, created_at, delivered_at, inspected_items, image_path } =
        data as ApiInspectedVirtualCardModel;
      setVirtualCard({ id, image_path, entry, created_at, delivered_at });
      setInspectedItems(inspected_items ?? []);
      setImagePath(`${process.env.BACKEND_SERVICE_URL}/${image_path}`);
    } else {
      alert("入力可能な名刺はありませんでした。トップページに戻ります。");
      window.location.href = "/";
    }
  };

  useEffect(() => {
    fetchEntry();
  }, []);

  const onSubmit = () => {
    fetchEntry();
  };

  return (
    <div key={virtualCard?.id}>
      {virtualCard ? (
        <div className="min-h-screen">
          <div className="row min-h-screen">
            <div className="col-md-6 flex items-center justify-center bg-[#ccc]">
              <Image
                src={imagePath}
                alt="Virtual Card"
                width={500}
                height={300}
              />
            </div>
            <div className="col-md-6 flex">
              <Form
                virtualCard={virtualCard}
                inspectedItems={inspectedItems}
                onSubmit={onSubmit}
                setVirtualCard={setVirtualCard}
              />
            </div>
          </div>
        </div>
      ) : (
        <div>
          <h1>入力対象の名刺がありません</h1>
        </div>
      )}
    </div>
  );
}
