import { fetchDeliveredVirtualCards } from "@/api/delivery";
import { ApiEntryItems } from "@/generated-client/Api";

const itemLabel: { [key in ApiEntryItems]: string } = {
  full_name: "名前",
  company_name: "会社名",
  position_name: "役職",
  email: "メールアドレス",
  address: "住所",
};

export default async function Page() {
  const virtualCard = await fetchDeliveredVirtualCards();

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold pb-2">データ化完了名刺一覧</h1>
      {virtualCard.success ? (
        <table className="table-fixed border rounded-xl">
          <thead className="border-b table-header-group">
            <tr className="text-gray-500">
              <th className="px-2">ID</th>
              <th className="px-2">{itemLabel["full_name"]}</th>
              <th className="px-2">{itemLabel["email"]}</th>
              <th className="px-2">{itemLabel["company_name"]}</th>
              <th className="px-2">{itemLabel["position_name"]}</th>
              <th className="px-2">{itemLabel["address"]}</th>
              <th className="px-2">納品日時</th>
            </tr>
          </thead>
          <tbody className="border-zinc-800">
            {virtualCard.data.map((card, index) => (
              <tr key={index} className="py-1 even:bg-gray-100 odd:bg-white">
                <td className="px-2 py-1">{card.id}</td>
                <td className="px-2 py-1">{card.entry.full_name}</td>
                <td className="px-2 py-1">{card.entry.email}</td>
                <td className="px-2 py-1">{card.entry.company_name}</td>
                <td className="px-2 py-1">{card.entry.position_name}</td>
                <td className="px-2 py-1">{card.entry.address}</td>
                <td className="px-2 py-1">{card.delivered_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>データ化が完了した名刺はありません</p>
      )}
    </div>
  );
}
