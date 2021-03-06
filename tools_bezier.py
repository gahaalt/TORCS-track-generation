from functools import reduce

import bezier
import matplotlib.pyplot as plt
import numpy as np


def get_vector(segment):
    return np.array(segment[1] - segment[0])


def get_track(points):
    segments = []
    curves = []
    for i in range(len(points) // 2):
        segments.append([points[2 * i], points[2 * i + 1]])

    segments = np.array(segments)
    for i in range(len(segments)):
        s1 = segments[i]
        s2 = segments[(i + 1) % len(segments)]

        v1 = 0.5 * get_vector(s1)
        v2 = 0.5 * get_vector(s2[::-1])

        nodes = np.vstack((s1[1], s1[1] + v1, s2[0] + v2, s2[0])).T

        curves.append(bezier.Curve(nodes, degree=3))

    return segments, curves


def draw_track(segments, curves):
    for s in segments:
        x_values = [s[0][0], s[1][0]]
        y_values = [s[0][1], s[1][1]]
        plt.plot(x_values, y_values)

    i = 0
    for c in curves:
        xs = [c.evaluate(x).T[0][0] for x in np.linspace(0, 1, 100)]
        ys = [c.evaluate(x).T[0][1] for x in np.linspace(0, 1, 100)]

        plt.plot(xs, ys)
        i += 1


def translate_curve(curve, K=50):
    vecs = []
    vals = []
    anses = []
    for i in np.linspace(0, 1, K + 1):
        # print(i)
        t = curve.evaluate_hodograph(i)
        tp = np.array([t[1], -t[0]])
        vecs += [tp]
        v = curve.evaluate(i)
        vals += [v]
        # print(v)

    for i in range(K):
        start_pos = vals[i]
        end_pos = vals[i + 1]
        start_vec = vecs[i]
        end_vec = vecs[i + 1]

        m = np.concatenate([start_vec, end_vec], axis=1)
        ans = np.linalg.inv(m) @ (end_pos - start_pos)

        d = np.linalg.det(m)

        p = start_pos + ans[0, 0] * start_vec

        v1 = p - start_pos
        v2 = p - end_pos

        r1 = np.linalg.norm(v1)
        r2 = np.linalg.norm(v2)

        hmm = max(-1, min(1, v1.T.dot(v2)[0][0] / (r1 * r2)))
        # print(hmm)
        arc = np.degrees(np.arccos(hmm))
        # print(arc)

        if hmm == 1:
            anses += [("Str", np.linalg.norm(start_pos - end_pos))]
        else:
            anses += [("Arc", r1, r2, arc, d > 0)]

    # for ans in anses:
    #     print(ans)
    return anses


def get_full_xml_track_file(track_name, xml_ready_segments, pit_stop=None):
    p = '' if pit_stop is None else str(pit_stop)
    l = '0.0' if pit_stop is None else str(15)
    w = '0.0' if pit_stop is None else str(5)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE params SYSTEM "../../../src/libs/tgf/params.dtd" [
<!--  general definitions for tracks  -->
<!ENTITY default-surfaces SYSTEM "../../../data/tracks/surfaces.xml">
]>

<params name="test" type="param" mode="mw">
  <section name="Surfaces">&default-surfaces;</section>
  <section name="Header">
    <attstr name="name" val="{track_name}" />
    <attstr name="category" val="evolution" />
    <attnum name="version" val="4" />
    <attstr name="author" val="Evolution" />
    <attstr name="description" val="Extremely Cool Track" />
  </section>
  <section name="Graphic">
    <attstr name="3d description" val="{track_name}.ac" />
    <section name="Terrain Generation">
      <attnum name="track step" unit="m" val="20" />
      <attnum name="border margin" unit="m" val="50" />
      <attnum name="border step" unit="m" val="30" />
      <attnum name="border height" unit="m" val="15" />
      <attstr name="orientation" val="clockwise" />
    </section>
  </section>
  <section name="Turn Marks">
    <attnum name="width" unit="m" val="1.0"/>
    <attnum name="height" unit="m" val="1.0"/>
    <attnum name="vertical space" unit="m" val="0.0"/>
    <attnum name="horizontal space" unit="m" val="2.0"/>
  </section>
  <section name="Main Track">
    <attnum name="width" unit="m" val="10.0" />
    <attnum name="profil steps length" unit="m" val="4.0" />
    <attstr name="surface" val="asphalt2-lines" />
    <!--Left part of track-->
    <section name="Left Side">
      <attnum name="start width" unit="m" val="4.0" />
      <attnum name="end width" unit="m" val="4.0" />
      <attstr name="surface" val="grass" />
    </section>
    <section name="Left Border">
      <attnum name="width" unit="m" val="0.5" />
      <attnum name="height" unit="m" val="0.05" />
      <attstr name="surface" val="curb-5cm-r" />
      <attstr name="style" val="plan" />
    </section>
    <section name="Left Barrier">
      <attnum name="width" unit="m" val="0.1" />
      <attnum name="height" unit="m" val="1.0" />
      <attstr name="surface" val="barrier" />
      <attstr name="style" val="curb" />
    </section>
    <!--End of left part-->
    <!--Right part of track-->
    <section name="Right Side">
      <attnum name="start width" unit="m" val="4.0" />
      <attnum name="end width" unit="m" val="4.0" />
      <attstr name="surface" val="grass" />
    </section>
    <section name="Right Border">
      <attnum name="width" unit="m" val="0.5" />
      <attnum name="height" unit="m" val="0.05" />
      <attstr name="surface" val="curb-5cm-r" />
      <attstr name="style" val="plan" />
    </section>
    <section name="Right Barrier">
      <attnum name="width" unit="m" val="0.1" />
      <attnum name="height" unit="m" val="1.0" />
      <attstr name="surface" val="barrier" />
      <attstr name="style" val="curb" />
    </section>
    <!--End of right part-->
    <section name="Pits">
      <attstr name="side" val="right" />
      <attstr name="entry" val="{p}" />
      <attstr name="start" val="{p}" />
      <attstr name="end" val="{p}" />
      <attstr name="exit" val="{p}" />
      <attnum name="length" unit="m" val="{l}" />
      <attnum name="width" unit="m" val="{w}" />
    </section>
    <section name="Track Segments">
        {xml_ready_segments}
    </section>
  </section>
</params>
"""


def fill_section_cur(id, left, deg, radius, end_radius, first=False):
    w = "rgt" if not left else "lft"
    m = """<attstr name="marks" val="50"/>""" if first else ''
    return f"""
<section name="curve {id}">
    <attstr name="type" val="{w}" />
    <attnum name="arc" unit="deg" val="{deg}" />
    <attnum name="radius" unit="m" val="{radius}" />
    <attnum name="end radius" unit="m" val="{end_radius}" />
    <attnum name="z start" unit="m" val="0.0" />
    <attnum name="z end" unit="m" val="0.0" />
    <attstr name="surface" val="asphalt2-lines" />
    {m}
    <!--Left part of segment-->
    <section name="Left Side">
        <attnum name="start width" unit="m" val="4.0" />
        <attnum name="end width" unit="m" val="4.0" />
        <attstr name="surface" val="grass" />
    </section>
    <section name="Left Border">
        <attnum name="width" unit="m" val="0.5" />
        <attnum name="height" unit="m" val="0.05" />
        <attstr name="surface" val="curb-5cm-r" />
        <attstr name="style" val="plan" />
    </section>
    <section name="Left Barrier">
        <attnum name="width" unit="m" val="0.1" />
        <attnum name="height" unit="m" val="1.0" />
        <attstr name="surface" val="barrier" />
        <attstr name="style" val="curb" />
    </section>
    <!--End of left part-->
    <!--Right part of segment-->
    <section name="Right Side">
        <attnum name="start width" unit="m" val="4.0" />
        <attnum name="end width" unit="m" val="4.0" />
        <attstr name="surface" val="grass" />
    </section>
    <section name="Right Border">
        <attnum name="width" unit="m" val="0.5" />
        <attnum name="height" unit="m" val="0.05" />
        <attstr name="surface" val="curb-5cm-r" />
        <attstr name="style" val="plan" />
    </section>
    <section name="Right Barrier">
        <attnum name="width" unit="m" val="0.1" />
        <attnum name="height" unit="m" val="1.0" />
        <attstr name="surface" val="barrier" />
        <attstr name="style" val="curb" />
    </section>
    <!--End of right part-->
    </section>
      """


def fill_section_str(id, length):
    return f"""
<section name="straight {id}">
    <attstr name="type" val="str" />
    <attnum name="lg" unit="m" val="{length}" />
    <attnum name="z start" unit="m" val="0.0" />
    <attnum name="z end" unit="m" val="0.0" />
    <attstr name="surface" val="asphalt2-lines" />
    <!--Left part of segment-->
    <section name="Left Side">
        <attnum name="start width" unit="m" val="4.0" />
        <attnum name="end width" unit="m" val="4.0" />
        <attstr name="surface" val="grass" />
    </section>
    <section name="Left Border">
        <attnum name="width" unit="m" val="0.5" />
        <attnum name="height" unit="m" val="0.05" />
        <attstr name="surface" val="curb-5cm-r" />
        <attstr name="style" val="plan" />
    </section>
    <section name="Left Barrier">
        <attnum name="width" unit="m" val="0.1" />
        <attnum name="height" unit="m" val="1.0" />
        <attstr name="surface" val="barrier" />
        <attstr name="style" val="curb" />
    </section>
    <!--End of left part-->
    <!--Right part of segment-->
    <section name="Right Side">
        <attnum name="start width" unit="m" val="4.0" />
        <attnum name="end width" unit="m" val="4.0" />
        <attstr name="surface" val="grass" />
    </section>
    <section name="Right Border">
        <attnum name="width" unit="m" val="0.5" />
        <attnum name="height" unit="m" val="0.05" />
        <attstr name="surface" val="curb-5cm-r" />
        <attstr name="style" val="plan" />
    </section>
    <section name="Right Barrier">
        <attnum name="width" unit="m" val="0.1" />
        <attnum name="height" unit="m" val="1.0" />
        <attstr name="surface" val="barrier" />
        <attstr name="style" val="curb" />
    </section>
    <!--End of right part-->
    </section>
      """


def get_len(s):
    return np.sqrt((s[1][0] - s[0][0]) ** 2 + (s[1][1] - s[0][1]) ** 2)


def to_xml(segments, curves):
    res = ""
    id = 0
    longest_straight = -1
    where = 0
    for i in range(len(segments)):
        l = get_len(segments[i]) * 100
        res += fill_section_str(id, l)
        if longest_straight < l:
            longest_straight = l
            where = id
        id += 1
        anses = translate_curve(curves[i], 100)

        for j in range(len(anses)):
            ans = anses[j]
            if ans[0] == "Arc":
                r1, r2, arc, left = ans[1:]
                res += fill_section_cur(id, left, arc, 100 * r1, 100 * r2, j==0)
                id += 1
            else:
                (length,) = ans[1:]
                res += fill_section_str(id, length * 100)
                id += 1

    where = None if longest_straight < 100 else "straight " + str(where)

    return res, where


def get_intersection_count(segments, curves, debug=False):
    def two_curves(fst, snd):
        intersections = fst.intersect(snd)
        if len(intersections[0, :]) > 0:
            s_vals = np.concatenate((intersections[0, :], intersections[1, :]))
            # print(s_vals)
            for i in s_vals:
                if i != 0 and i != 1:
                    return True
        return False

    def segment_to_curve(bg, en):
        nodes = np.asfortranarray([
            [bg[0], en[0]],
            [bg[1], en[1]]
        ])
        return bezier.Curve(nodes, degree=1)

    def self_cross(curve):
        parts = 100
        pt = np.linspace(0, 1, parts + 1)
        mini_curves = [curve.specialize(a, b) for (a, b) in zip(pt, pt[1:])]
        y = len(mini_curves)
        for i in range(y):
            for j in range(i + 1, y):
                if two_curves(mini_curves[i], mini_curves[j]): return True
        return False

    cnts = 0

    pts = reduce(lambda a, b: a + b, [[(s[0][0], s[0][1]), (s[1][0], s[1][1])] for s in segments], [])
    pts_set = set(pts)

    if len(pts_set) != len(pts): cnts += (len(pts) - len(pts_set))

    sgms = list(map(lambda s: segment_to_curve(s[0], s[1]), segments))
    all_parts = sgms + curves

    for c in curves:
        if self_cross(c):
            if debug: draw_track([], [c])
            # return True
            cnts += 1

    for i in range(len(all_parts)):
        for j in range(i + 1, len(all_parts)):
            s = all_parts[i]
            t = all_parts[j]
            if two_curves(s, t):
                if debug: draw_track([], [s, t])
                # return True
                cnts += 1

    return cnts


def get_curve_stats(curve, K = 50):
    vecs = []
    vals = []
    turns = []
    lengths = []
    for i in np.linspace(0,1, K + 1):
        t = curve.evaluate_hodograph(i)
        tp = np.array([t[1], -t[0]])
        vecs += [tp]
        v = curve.evaluate(i)
        vals += [v]

    for i in range(K):
        start_pos = vals[i]
        end_pos = vals[i+1]
        start_vec = vecs[i]
        end_vec = vecs[i+1]

        cut = curve.specialize(i / K, (i + 1) / K)

        m = np.concatenate([start_vec, end_vec], axis=1)
        ans = np.linalg.inv(m) @ (end_pos - start_pos)

        d = np.linalg.det(m)

        p = start_pos + ans[0,0] * start_vec

        v1 = p - start_pos
        v2 = p - end_pos

        r1 = np.linalg.norm(v1)
        r2 = np.linalg.norm(v2)


        if max(-1, min(1, v1.T.dot(v2)[0][0] / (r1 * r2))) == 1:
            turns.append(0)
            lengths.append(np.linalg.norm(start_pos - end_pos))
        else:
            turns.append(1 / ((r1 + r2) / 2) * np.sign(d))
            lengths.append(cut.length)

    return turns, lengths


def get_track_stats(segments, curves):
    turns = []
    lengths = []
    for s in segments:
        turns.append(0)
        lengths.append(get_len(s))
    for c in curves:
        t, l = get_curve_stats(c)
        turns += t
        lengths += l

    return turns, lengths
