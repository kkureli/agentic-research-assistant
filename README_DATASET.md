# Agentic RAG Sample Dataset

Bu dataset tamamen sentetiktir ve eğitim / portfolio amaçlı Agentic RAG projesinde kullanılmak üzere oluşturulmuştur.

## İçerik
- Asteria Cloud Systems: FY2025, Q1 2026, Q2 2026, strategy memo, analyst risk notes
- Nova Mobility: FY2025, Q1 2026, Q2 2026, strategy memo
- 2 sektör raporu
- 1 methodology dokümanı
- 20 başlangıç evaluation sorusu

## Neden Sentetik?
- Kontrollü ground-truth sağlar.
- Çok dokümanlı karşılaştırma, metadata filtering ve citation verification test edilebilir.
- Benzer ama farklı riskler ve metrikler içerir; entity mixing hatalarını yakalamaya yardımcı olur.

## Önerilen Kullanım
`data/` klasörünü projenin root'undaki `data/` klasörüyle birleştir.
`evals/questions.jsonl` dosyasını evaluation pipeline'ında kullan.
