# MyApp

ユーザーが短い文章を投稿をして、他のユーザーとリアルタイムでコミュニケーションを取ることができるアプリ。

## 目標

このプロジェクトの主な目標は、Webアプリケーションを制作することでフロントエンドとバックエンドの役割を理解し、以下の技術を習得することです。

- Flask: 軽量なPythonのWebフレームワーク
- Flet: フロントエンドのUIを簡単に作成できるツール (Pythonだけで書けるFlutterベースのGUIフレームワーク)
- SQL: データベース操作の基礎知識とスキル
- ユーザー登録・ログイン機能: Firebaseなどの外部サービスを使用せずに実装
- ...

## 仕様

このアプリケーションは、ユーザー登録とログイン機能を備えた基本的なWebアプリケーションです。バックエンドはFlaskで構築されており、フロントエンドはFletを使用して作成されています。データベースにはSQLを使用し、ユーザーのデータを管理します。

### 機能

1. **ユーザー登録**: 新規ユーザーがアカウントを作成できます。
2. **ログイン**: 登録したアカウントからログインできます。
3. **タイムライン**: 他のユーザーの投稿を見ることができます。
4. **検索**: ユーザーまたは投稿を検索できます。検索バーの左のアイコンからユーザー/投稿の切り替えができます。
5. **通知**(実装予定): 他人からのアクションがあった場合ここに通知します。
6. **メッセージ**(実装予定): ほかのユーザーと一対一でやり取りができます。
7. **AIチャット**: AIとお喋りができます
8. **プロフィール**: 自分のプロフィールの表示・編集ができます。また、自分の過去の投稿も確認できます。
9. **設定**(実装予定): アプリの設定ができます。
10. **投稿**: 入力した内容を投稿できます。投稿は他人に表示されます。


## 使用方法

このプロジェクトをローカル環境で動作させるための手順は以下の通りです。

### 前提条件

- Python 3.x がインストールされていることを確認してください。
- FlaskとFletをインストールします。

    ```bash
    pip install flask flet
    ```

### 起動手順

1. **APIの起動**: `api.py` を実行してバックエンドのAPIサーバーを起動します。

    ```bash
    python3 api.py
    ```

2. **フロントエンドの起動**: `main.py` を実行してFletアプリケーションを起動します。

    ```bash
    flet run main.py -w -p 44444
    ```

3. **アプリケーションにアクセス**: ウェブブラウザで以下のURLにアクセスします。

    ```
    https://yokohama-uwu.love/flet/
    ```

## ディレクトリ構成

## 今後の計画

## 貢献

## ライセンス


---
