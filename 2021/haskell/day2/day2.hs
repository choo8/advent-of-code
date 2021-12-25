#!/usr/bin/env cabal
{- cabal:
       build-depends: base ^>=4.14.3.0, text, mtl
-}

module Main where

import Control.Monad.State

type Position = (Int, Int)
type PositionNew = (Int, Int, Int)

main :: IO ()
main = do
    contents <- getContents
    putStrLn $ "Part 1: " ++ (show $ part1 contents) ++ " Part 2: " ++ (show $ part2 contents)

readInt :: String -> Int
readInt = read

processAction :: String -> (String, Int)
processAction x = (dir, readInt mag)
    where [dir, mag] = words x

processCommands :: [(String, Int)] -> State Position Int
processCommands [] = do
    (h, d) <- get
    return (h * d)
processCommands (x:xs) = do
    (h, d) <- get
    case (fst x) of
        "forward" -> put (h + (snd x), d)
        "down" -> put (h, d + (snd x))
        "up" -> put (h, d - (snd x))
    processCommands xs

part1 :: String -> Int
part1 xs = evalState (processCommands (map processAction $ lines xs)) (0, 0)

processCommandsNew :: [(String, Int)] -> State PositionNew Int
processCommandsNew [] = do
    (h, d, _) <- get
    return (h * d)
processCommandsNew (x:xs) = do
    (h, d, a) <- get
    case (fst x) of
        "forward" -> put (h + (snd x), d + (a * (snd x)), a)
        "down" -> put (h, d, a + (snd x))
        "up" -> put (h, d, a - (snd x))
    processCommandsNew xs

part2 :: String -> Int
part2 xs = evalState (processCommandsNew (map processAction $ lines xs)) (0, 0, 0)