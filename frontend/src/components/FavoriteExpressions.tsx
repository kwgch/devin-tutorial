import { FavoriteExpression } from '../types';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';

interface FavoriteExpressionsProps {
  expressions: FavoriteExpression[];
}

export function FavoriteExpressions({ expressions }: FavoriteExpressionsProps) {
  if (expressions.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>お気に入りの表現</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500">保存された表現はまだありません。</p>
          <p className="text-sm text-gray-400 mt-2">
            日記の詳細画面でテキストを選択して表現を保存できます。
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>お気に入りの表現</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {expressions.map((expr, index) => (
            <div key={index} className="p-3 border rounded-md">
              <div className="flex flex-wrap gap-2 mb-2">
                <Badge variant="outline" className="bg-blue-50">
                  {expr.japanese_text}
                </Badge>
                <Badge variant="outline" className="bg-green-50">
                  {expr.english_text}
                </Badge>
              </div>
              {expr.note && <p className="text-sm text-gray-600">{expr.note}</p>}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
