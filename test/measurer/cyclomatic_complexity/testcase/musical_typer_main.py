"""
Notice: This file is from "musical-typer", which the author of "wow-thats-big" wrote.

This is just a source code for the testing, so you can ignore errors and warnings
generated from this file.

Expected value for each function:
   gs_specify_score()     -> 3
   gs_main_routine()      -> 50
   gs_result()            -> 11
   gs_special_error_log() -> 8

Expected value for average: 18.0
"""

##############################
#                            #
#   loxygenK/musical_typer   #
#   メインプログラム         #
#   (c)2020 loxygenK         #
#      All rights reversed.   #
#                            #
##############################

import sys
import os

# Python管理ライブラリ
import math
import pygame
from pygame.locals import *

# Pygame初期化
pygame.mixer.pre_init(44100, 16, 2, 1024)
pygame.mixer.init()
pygame.init()

# 自作ライブラリ
from lib import DrawMethodTemplates
from lib.GameSystem import *
from lib.ColorTheme import *

# FPS管理用インスタンスを生成
fps_clock = pygame.time.Clock()


def gs_specify_score():
    # ----- [ ゲーム用の情報準備 ] -----

    if len(sys.argv) < 2:
        raise RuntimeError("Song is not specified!")
    elif not os.path.isfile(sys.argv[1]):
        raise FileNotFoundError("Specified path is not file, or not exists!")
    else:
        print("Game will start at soon. Stay tuned!")

    # 譜面を読み込む
    score_data = Score()
    score_data.read_score(sys.argv[1])

    return score_data


def gs_main_routine(score_data: Score):
    # ゲームに必要なインスタンスを生成

    ui = Screen()
    game_info = GameInfo(score_data)
    keyboard_drawer = DrawingUtil.KeyboardDrawer(ui.screen, 193, ui.full_font, 40, 5, 2)

    # ループ管理用変数
    game_finished_reason = ""
    mainloop_continues = True

    # フレームカウンター
    # 点滅処理などに使う
    frame_count = 0

    # スクリーンのサイズを取得
    w, h = ui.screen_size

    # 次の歌詞を表示するモードに居るか
    is_tmp_next_lyrics_printing = False
    is_cont_next_lyrics_printing = False

    # ランク決定用定数
    rank_standard = [200, 150, 125, 100, 99.50, 99, 98, 97, 94, 90, 80, 60, 40, 20, 10, 0]
    rank_string = ["Wow", "Unexpected", "Very God", "God", "Pro", "Genius", "Geki-tsuyo", "tsuyotusyo", "AAA", "AA",
                   "A", "B", "C", "D", "E", "F"]
    # ----- [ ゲーム準備 ] -----

    # 再生
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(1)

    game_info.pos = 0

    # メインループ
    # (何らかの理由で強制的にメインループを抜ける必要が出てきた or 曲が終わった)
    while mainloop_continues and pygame.mixer.music.get_pos() >= 0:

        # -----------------
        #    事前計算
        # -----------------

        # フレームカウンタを更新
        frame_count = (frame_count + 1) % 60
        # 曲上の現在位置を把握
        game_info.pos = pygame.mixer.music.get_pos() / 1000

        # 現在の歌詞・ゾーン・セクションを取得
        lyx_idx = game_info.update_current_lyrincs()
        game_info.update_current_zone()
        sct_idx = game_info.get_current_section()

        # ---------------------------
        #   イベント処理／ジャッジ
        # ---------------------------

        # イベント処理ループ
        for event in pygame.event.get():
            if event.type == QUIT:
                mainloop_continues = False
                break
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    is_tmp_next_lyrics_printing = False

            if event.type == KEYDOWN:

                # ESCキーの場合
                if event.key == K_ESCAPE:
                    mainloop_continues = False
                    break

                if event.key == K_SPACE:
                    is_tmp_next_lyrics_printing = True

                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    is_cont_next_lyrics_printing = not is_cont_next_lyrics_printing

                # 大前提として、無効なキーが押されていないか
                if Romautil.is_readable_key_pressed(event.key):

                    # これ以上打つキーがない(打ち終わったか、そもそも歌詞がない)
                    if game_info.completed:
                        SoundEffectConstants.unneccesary.play()
                        continue

                    # 正しいキーが押されたか
                    if game_info.is_expected_key(chr(event.key)):

                        # 輪唱で初めての打鍵か
                        if game_info.full[:1] and game_info.sent_count == 0:
                            game_info.override_key_prev_pos()

                        # 成功処理をする
                        got_point = game_info.count_success()

                        # 成功エフェクト
                        ui.add_fg_effector(30, "AC/WA", DrawMethodTemplates.slide_fadeout_text,
                                           ["Pass", more_blackish(GREEN_THIN_COLOR, 50), ui.alphabet_font, 10, -150,
                                            -383])

                        if not (is_cont_next_lyrics_printing or is_tmp_next_lyrics_printing):
                            # キーボード上に点数を描画する
                            x, y = keyboard_drawer.get_place(chr(event.key))
                            x += keyboard_drawer.key_size / 2
                            x -= ui.full_font.render("+{}".format(got_point), True, TEXT_COLOR).get_width() / 2
                            ui.add_fg_effector(30, chr(event.key), DrawMethodTemplates.absolute_fadeout,
                                               ["+{}".format(got_point), BLUE_THICK_COLOR, ui.full_font, 15, x, y])

                        # AC／WAのエフェクト
                        if game_info.is_ac:
                            ui.add_fg_effector(120, "AC/WA", DrawMethodTemplates.slide_fadeout_text,
                                               ["AC", GREEN_THICK_COLOR, ui.alphabet_font, 20, -170, -383])
                            ui.add_bg_effector(15, "AC/WA", DrawMethodTemplates.blink_rect,
                                               [more_whitish(GREEN_THIN_COLOR, 50), (0, 60, w, 130)])
                            SoundEffectConstants.ac.play()
                        elif game_info.is_wa:
                            ui.add_fg_effector(120, "AC/WA", DrawMethodTemplates.slide_fadeout_text,
                                               ["WA", more_whitish(BLUE_THICK_COLOR, 100), ui.alphabet_font, 20, -170,
                                                -383])
                            ui.add_bg_effector(15, "AC/WA", DrawMethodTemplates.blink_rect,
                                               [more_whitish(BLUE_THICK_COLOR, 100), (0, 60, w, 130)])
                            SoundEffectConstants.wa.play()
                        else:
                            if game_info.is_in_zone and game_info.score.zone[game_info.zone_index]:
                                SoundEffectConstants.special_success.play()
                            else:
                                if game_info.get_key_per_second() > 4:
                                    SoundEffectConstants.fast.play()
                                else:
                                    SoundEffectConstants.success.play()
                    else:

                        if not game_info.has_to_prevent_miss:
                            # 失敗をカウントする
                            game_info.count_failure()

                            # 効果音を流す
                            SoundEffectConstants.failed.play()

                            # エフェクト

                            ui.add_bg_effector(15, "AC/WA", DrawMethodTemplates.blink_rect,
                                               [(255, 200, 200), (0, 60, w, 130)])
                            ui.add_fg_effector(30, "AC/WA", DrawMethodTemplates.slide_fadeout_text,
                                               ["MISS", more_whitish(RED_COLOR, 50), ui.alphabet_font,
                                                10, -150, -383])
                        else:
                            SoundEffectConstants.unneccesary.play()

        # ------------
        #     計算
        # ------------

        # ===== 歌詞情報が変化したときの処理 =====

        # 歌詞が変わった?
        if lyx_idx:

            # TLEの計算をする
            game_info.apply_TLE()

            # 最終的なタイプ情報を記録する
            game_info.sentence_log.append([game_info.sent_count, game_info.sent_miss, game_info.completed])

            # TLEした?
            if len(game_info.target_roma) > 0 and not game_info.has_to_prevent_miss:
                ui.add_fg_effector(30, "TLE", DrawMethodTemplates.slide_fadeout_text,
                                   ["TLE", more_blackish(RED_COLOR, 50), ui.alphabet_font, -10,
                                    -150, -383])
                ui.add_bg_effector(15, "TLE", DrawMethodTemplates.blink_rect,
                                   [more_whitish(RED_COLOR, 50), (0, 60, w, 130)])
                SoundEffectConstants.tle.play()
            else:
                # 歌詞が変わるまでの待機時間を考慮して、前回のキータイプ時間を早める
                game_info.override_key_prev_pos()

            # 歌詞をアップデートする
            game_info.update_current_lyrics()

            # 曲が終わった?
            if game_info.song_finished:
                # 歌詞情報を消去する
                game_info.update_current_lyrics("", "")
                ui.add_bg_effector(60, "S.F.", DrawMethodTemplates.slide_fadeout_text,
                                   ["Song Finished!", (255, 127, 0), ui.system_font, 25, 0, 0])

        # セクションが変わった?
        if sct_idx:

            # セクションを全完した?
            if game_info.section_miss == 0 and game_info.section_count != 0:
                # エフェクトとボーナスポイント
                ui.add_bg_effector(60, "Section AC", DrawMethodTemplates.slide_fadeout_text,
                                   ["Section AC!", (255, 127, 0), ui.system_font, 25, 0, 0])
                game_info.point += game_info.SECTION_PERFECT_POINT

            # セクションごとのタイプ情報を記録
            game_info.section_log.append([game_info.section_count, game_info.section_miss])

            # セクションのデータを削除
            game_info.reset_section_score()

        # ---------------
        #     画面描画
        # ----------------

        # [ 背面レイヤー ]

        # 画面を消去する
        ui.screen.fill(BACKGROUND_COLOR)

        # 曲のタイトルなどの情報
        DrawingUtil.write_limit(ui.screen, (w - 2, 0), w / 2, ui.alphabet_font, score_data.properties["title"])
        DrawingUtil.write_limit(ui.screen, (w - 5, 33), w / 2, ui.system_font,
                                score_data.properties["song_author"] + "／" + score_data.properties["singer"],
                                more_whitish(TEXT_COLOR, 100))

        # 残り時間ゲージ
        pygame.draw.rect(ui.screen, more_blackish(BACKGROUND_COLOR, 25), (0, 60, w, 130))
        pygame.draw.rect(ui.screen, more_blackish(BACKGROUND_COLOR, 50),
                         (0, 60, math.floor(game_info.get_time_remain_ratio() * w), 130))

        # レイヤーが変わるのでここで背景エフェクトを更新する
        ui.update_effector(1)

        # ----- [ 前面レイヤー ] -----

        # 歌詞

        if game_info.full[:1] != "/" or game_info.sent_count > 0:
            DrawingUtil.print_progress(ui.screen, (w / 2, 80), MARGIN + 20, ui.nihongo_font,
                                       game_info.typed_kana, game_info.target_kana)
            DrawingUtil.print_progress(ui.screen, (w / 2, 130), MARGIN + 5, ui.full_font,
                                       game_info.typed_roma, game_info.target_roma)

            printout_lyrics = game_info.full if game_info.full[:1] != "/" else game_info.full[1:]

            ui.print_str(MARGIN - 12, 60, ui.full_font, printout_lyrics, more_whitish(TEXT_COLOR, 30))

        # コンボ
        combo_text = ui.full_font.render(str(game_info.combo), True, more_whitish(TEXT_COLOR, 50))
        ui.screen.blit(combo_text, (MARGIN - 12, 157))
        ui.print_str(combo_text.get_width() + 5, 165, ui.system_font, "chain", more_whitish(TEXT_COLOR, 75))

        # 正確率ゲージ
        pygame.draw.rect(ui.screen, GREEN_THICK_COLOR if not game_info.is_ac else RED_COLOR,
                         (0, 60, w * game_info.get_sentence_accuracy(), 3))
        DrawingUtil.write_limit(ui.screen, (w * game_info.get_rate(limit=True), 168), 0, ui.system_font,
                                rank_string[game_info.calculate_rank()], more_whitish(TEXT_COLOR, 100))

        # 達成率ゲージ
        if game_info.calculate_rank() > 0:
            acheive_rate = rank_standard[game_info.calculate_rank() - 1] / 100
            pygame.draw.rect(ui.screen, RED_COLOR, (0, 187, w * acheive_rate, 3))
        pygame.draw.rect(ui.screen, GREEN_THICK_COLOR if game_info.get_rate() < 0.8 else BLUE_THICK_COLOR,
                         (0, 187, w * game_info.get_rate(), 3))

        # キーボード

        if is_tmp_next_lyrics_printing or is_cont_next_lyrics_printing:
            for i in range(3):
                lyrics_index = (i + game_info.lyrincs_index + 1)
                if lyrics_index >= len(game_info.score.score):
                    break
                ui.print_str(5, 193 + 60 * i, ui.system_font, "[{}]".format(lyrics_index), TEXT_COLOR)

                if game_info.score.score[lyrics_index][1][:1] != "/":
                    ui.print_str(5, 210 + 60 * i, ui.full_font, game_info.score.score[lyrics_index][1], TEXT_COLOR)
                    ui.print_str(5, 230 + 60 * i, ui.system_font,
                                 Romautil.hira2roma(game_info.score.score[lyrics_index][2]),
                                 more_whitish(TEXT_COLOR, 50))
        else:
            if game_info.has_to_prevent_miss:
                keyboard_drawer.draw("", background_color=(192, 192, 192))
            else:
                keyboard_drawer.draw(game_info.target_roma[:1],
                                     background_color=(192, 192, 192) if game_info.completed else None)

        # 点数表示
        if game_info.point < 0:
            if frame_count % 20 < 10:
                score_color = RED_COLOR
            else:
                score_color = BLUE_THICK_COLOR
            ui.print_str(5, 20, ui.alphabet_font, "{:08d}".format(game_info.point), score_color)
        else:
            ui.print_str(5, 20, ui.alphabet_font, "{:08d}".format(game_info.point), BLUE_THICK_COLOR)

        # --- リアルタイム情報 ---
        pygame.draw.line(ui.screen, more_whitish(TEXT_COLOR, 100), (0, 375), (w, 375), 2)

        # タイピング速度
        ui.print_str(MARGIN, 382, ui.system_font, "タイピング速度", more_whitish(TEXT_COLOR, 100))
        if game_info.get_key_per_second() > 4:
            color = more_blackish(RED_COLOR, 30 if frame_count % 10 < 5 else 0)
            pygame.draw.rect(ui.screen, color, (MARGIN, 400, w - MARGIN * 2, 20))
        else:
            pygame.draw.rect(ui.screen, GREEN_THIN_COLOR, (MARGIN, 400, w - MARGIN * 2, 20))
            pygame.draw.rect(ui.screen, more_blackish(GREEN_THIN_COLOR, 50),
                             (MARGIN, 400, game_info.get_key_per_second() / 4 * (w - MARGIN * 2), 20))

        DrawingUtil.write_center_x(ui.screen, w / 2, 398, ui.system_font,
                                   "{:4.2f} Char/sec".format(game_info.get_key_per_second()), TEXT_COLOR)

        # 正確率の数値情報
        ui.print_str(MARGIN, 430, ui.system_font, "正確率", more_whitish(TEXT_COLOR, 100))

        pygame.draw.rect(ui.screen, more_blackish(RED_COLOR, 50),
                         (MARGIN + 5, 510, game_info.get_full_accuracy() * 250, 3))
        ui.print_str(MARGIN + 5, 430, ui.big_font, "{:05.1f}％".format(game_info.get_full_accuracy() * 100),
                     tuple(x * game_info.get_full_accuracy() for x in RED_COLOR))

        # ランク
        ui.print_str(MARGIN + 320, 430, ui.system_font, "達成率", more_whitish(TEXT_COLOR, 100))
        ui.print_str(MARGIN + 330, 430, ui.big_font, "{:05.1f}％".format(game_info.get_rate() * 100), BLUE_THICK_COLOR)

        # レイヤーが変わるのでここで前面エフェクトを更新する
        ui.update_effector(0)

        # FPSカウンタ
        ui.print_str(3, -3, ui.system_font, "{:5.2f} fps".format(fps_clock.get_fps()), TEXT_COLOR)

        # ループ終わり
        fps_clock.tick(60)
        pygame.display.update()

    # メインループ終了
    print("*****************")
    print("* LOOP FINISHED *")
    print("*****************")
    print(mainloop_continues)
    print(game_finished_reason)

    pygame.mixer.music.stop()

    return game_info


def gs_result(game_info):
    ui = Screen()
    w, h = ui.screen_size
    mainloop_continues = True
    retry = False
    rank_standard = [200, 150, 125, 100, 99.50, 99, 98, 97, 94, 90, 80, 60, 40, 20, 10, 0]
    rank_string = ["Wow", "Unexpected", "Very God", "God", "Pro", "Genius", "Geki-tsuyo", "tsuyotusyo", "AAA", "AA",
                   "A", "B", "C", "D", "E", "F"]

    while mainloop_continues:
        for event in pygame.event.get():
            if event.type == QUIT:
                mainloop_continues = False
                break
            if event.type == KEYDOWN:
                # ESCキーの場合
                if event.key == K_ESCAPE:
                    mainloop_continues = False
                    break
                elif event.key == K_r:
                    retry = True
                    mainloop_continues = False
                    break

        ui.screen.fill(BACKGROUND_COLOR)

        # 曲のタイトルなどの情報
        ui.print_str(MARGIN, 0, ui.nihongo_font, score.properties["title"], TEXT_COLOR)
        ui.print_str(MARGIN, 50, ui.full_font,
                     score.properties["song_author"] + "／" + score.properties["singer"],
                     more_whitish(TEXT_COLOR, 25))

        pygame.draw.line(ui.screen, more_whitish(TEXT_COLOR, 100), (0, 90), (w, 90), 2)

        ui.print_str(MARGIN, 85, ui.big_font,
                     rank_string[game_info.calculate_rank()],
                     more_blackish(RED_COLOR, 150 * (game_info.calculate_rank() + 1) / len(rank_standard)))

        ui.print_str(MARGIN, 150, ui.nihongo_font, "{:06.2f}％".format(game_info.get_rate() * 100),
                     tuple(x * game_info.get_full_accuracy() for x in RED_COLOR))

        if game_info.get_key_per_second() > 4:
            pygame.draw.rect(ui.screen, more_blackish(RED_COLOR, 30), (MARGIN, 210, w - MARGIN * 2, 20))
        else:
            pygame.draw.rect(ui.screen, GREEN_THIN_COLOR, (MARGIN, 210, w - MARGIN * 2, 20))
            pygame.draw.rect(ui.screen, more_blackish(GREEN_THIN_COLOR, 50),
                             (MARGIN, 210, game_info.get_key_per_second() / 4 * (w - MARGIN * 2), 20))

        DrawingUtil.write_center_x(ui.screen, w / 2, 208, ui.system_font,
                                   "{:4.2f} Char/sec".format(game_info.get_key_per_second()), TEXT_COLOR)

        if game_info.calculate_rank() > 0:
            acheive_rate = rank_standard[game_info.calculate_rank() - 1] - game_info.get_rate() * 100
            ui.print_str(MARGIN + 200, 160, ui.system_font,
                         "{} まで ".format(rank_string[game_info.calculate_rank() - 1]), BLUE_THICK_COLOR)
            ui.print_str(MARGIN + 200, 168, ui.alphabet_font, "{:06.2f}% ".format(acheive_rate), BLUE_THICK_COLOR)

        ui.print_str(MARGIN, 240, ui.system_font, "正確率", more_whitish(TEXT_COLOR, 50))
        ui.print_str(MARGIN + 10, 247, ui.nihongo_font, "{:06.2f}%".format(game_info.get_full_accuracy() * 100),
                     tuple(x * game_info.get_full_accuracy() for x in RED_COLOR))

        DrawingUtil.write_limit(ui.screen, (w - 15, 150), w / 2, ui.nihongo_font, "{:08}".format(game_info.point))

        pygame.draw.line(ui.screen, more_whitish(TEXT_COLOR, 100), (0, 320), (w, 320), 2)

        # TODO: 21世紀史上もっともひどいデザインをどうにかする
        ui.print_str(MARGIN - 10, 320, ui.alphabet_font, "[R]／リトライ", TEXT_COLOR)
        ui.print_str(MARGIN + 300, 320, ui.alphabet_font, "[Esc]／終了", TEXT_COLOR)

        fps_clock.tick(60)
        pygame.display.update()

    return retry


def gs_special_error_log(score_data, path):
    ui = Screen()
    w, h = ui.screen_size

    error_index = 0

    mainloop_continues = True
    while mainloop_continues:
        for event in pygame.event.get():
            if event.type == QUIT:
                mainloop_continues = False
                break
            if event.type == KEYDOWN:
                # ESCキーの場合
                if event.key == K_ESCAPE:
                    mainloop_continues = False
                    break
                if event.key == K_UP:
                    error_index = max(0, error_index - 1)
                if event.key == K_DOWN:
                    error_index = min(error_index + 1, len(score_data.log) - 1)

        ui.screen.fill(BACKGROUND_COLOR)

        ui.print_str(MARGIN - 10, 0, ui.alphabet_font, "読み込みに失敗しました！", RED_COLOR)
        ui.print_str(MARGIN - 10, 35, ui.system_font, "譜面がおかしなことになっているようです:", RED_COLOR)
        ui.print_str(MARGIN - 10, 60, ui.system_font, path, TEXT_COLOR)

        pygame.draw.line(ui.screen, more_whitish(TEXT_COLOR, 100), (0, 83), (w, 83), 2)

        ui.print_str(MARGIN, 90, ui.system_font, score_data.log[0][1], TEXT_COLOR)
        ui.print_str(MARGIN, 105, ui.alphabet_font, score_data.log[0][2], TEXT_COLOR)

        pygame.draw.line(ui.screen, more_whitish(TEXT_COLOR, 100), (0, 160), (w, 160), 2)

        fps_clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':

    try:
        score = gs_specify_score()

        loop_continues = True
        while loop_continues:
            game_result = gs_main_routine(score)
            loop_continues = gs_result(game_result)
    finally:
        pygame.quit()
